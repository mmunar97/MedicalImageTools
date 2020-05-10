import cv2
import numpy
import threading

from typing import Callable, Tuple

from Controller.ListenerCode import ListenerCode
from Model.DicomSelectedFile import DicomSelectedFile


class DicomModel(threading.Thread):

    def __init__(self, listener: Callable):
        threading.Thread.__init__(self)

        self.__listener = listener

        self.__first_image_file: DicomSelectedFile = None
        self.__second_image_file: DicomSelectedFile = None

    def set_picked_files(self, first_image_file: DicomSelectedFile, second_image_file: DicomSelectedFile):
        """
        Sets the picked files.

        Args:
            first_image_file: The first picked image, represented as DicomSelectedFile.
            second_image_file: The second image, represented as DicomSelectedFile.
        """
        self.__first_image_file = first_image_file
        self.__second_image_file = second_image_file

        try:
            self.__first_image_file.read()
            self.__second_image_file.read()

            self.__listener(ListenerCode.IMAGES_READ, status=1, upper_limit=self.get_tensor_limit_for_axis(0))
        except Exception:
            self.__listener(ListenerCode.IMAGES_READ, status=-1)

    def get_tensor_limit_for_axis(self, axis: int) -> int:
        """
        Returns the maximum shape value from two tensors.

        Args:
            axis: An integer, representing the axis.

        Returns:
            An integer.
        """
        limit1 = self.__first_image_file.image_tensor.shape[axis]
        limit2 = self.__second_image_file.image_tensor.shape[axis]

        return max(limit1, limit2)

    def get_tensor_images(self, axis: int, slice: int,
                          alpha: int) -> Tuple[numpy.ndarray, numpy.ndarray, numpy.ndarray]:
        """
        Returns the images to be shown and the alpha-combination of both.

        Args:
            axis: An integer, representing the axis.
            slice: An integer, representing the slice.
            alpha: An integer, representing the alpha value.

        Returns:
            A tuple of three images.
        """
        image1_limit = self.__first_image_file.image_tensor.shape[axis]
        image2_limit = self.__second_image_file.image_tensor.shape[axis]

        image1: numpy.ndarray = None
        image2: numpy.ndarray = None

        if axis == 0:
            image1 = self.__first_image_file.image_tensor[min(slice, image1_limit-1), :, :]
            image2 = self.__second_image_file.image_tensor[min(slice, image2_limit-1), :, :]
        elif axis == 1:
            image1 = self.__first_image_file.image_tensor[:, min(slice, image1_limit-1), :]
            image2 = self.__second_image_file.image_tensor[:, min(slice, image2_limit-1), :]
        elif axis == 2:
            image1 = self.__first_image_file.image_tensor[:, :, min(slice, image1_limit-1)]
            image2 = self.__second_image_file.image_tensor[:, :, min(slice, image2_limit-1)]

        image1 = self.__resize_image(image1, size=(300, 300), background_color=127)
        image2 = self.__resize_image(image2, size=(300, 300), background_color=127)

        alpha_image = (1-alpha/100)*image1+(alpha/100)*image2

        return image1, image2, alpha_image

    @staticmethod
    def __resize_image(image: numpy.ndarray, size: Tuple[int, int], background_color: int = 0) -> numpy.ndarray:
        """
        Resizes one image and crops with a certain color the missing space.

        Args:
            image: An image, represented as a numpy array.
            size: A tuple of two elements, representing the new size.
            background_color: An integer, representing the grayscale color.

        Returns:
            A resized image.
        """
        height, width = image.shape[:2]
        conv_height, conv_width = size

        if height > conv_height or width > conv_width:
            interpolation_method = cv2.INTER_AREA
        else:
            interpolation_method = cv2.INTER_CUBIC

        aspect = width/height

        if aspect > 1:
            new_width = conv_width
            new_height = numpy.round(new_width/aspect).astype(int)

            padding_vertical = (conv_height - new_height) / 2
            padding_top, padding_bottom = numpy.floor(padding_vertical).astype(int), numpy.ceil(padding_vertical).astype(int)
            padding_left, padding_right = 0, 0
        elif aspect < 1:
            new_height = conv_height
            new_width = numpy.round(new_height*aspect).astype(int)
            padding_horizontal = (conv_width - new_width) / 2
            padding_left, padding_right = numpy.floor(padding_horizontal).astype(int), numpy.ceil(padding_horizontal).astype(int)
            padding_top, padding_bottom = 0, 0
        else:
            new_height, new_width = conv_height, conv_width
            padding_left, padding_right, padding_top, padding_bottom = 0, 0, 0, 0

        if len(image.shape) is 3 and not isinstance(background_color, (list, tuple, numpy.ndarray)):
            background_color = [background_color] * 3

        scaled_img = cv2.resize(image, (new_width, new_height), interpolation=interpolation_method)
        scaled_img = cv2.copyMakeBorder(scaled_img, padding_top, padding_bottom, padding_left, padding_right,
                                        borderType=cv2.BORDER_CONSTANT, value=background_color)

        return scaled_img



