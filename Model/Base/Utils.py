import cv2
import numpy

from typing import Tuple


def resize_image(image: numpy.ndarray, size: Tuple[int, int], background_color: int = 0) -> numpy.ndarray:
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

    aspect = width / height

    if aspect > 1:
        new_width = conv_width
        new_height = numpy.round(new_width / aspect).astype(int)

        padding_vertical = (conv_height - new_height) / 2
        padding_top, padding_bottom = numpy.floor(padding_vertical).astype(int), numpy.ceil(padding_vertical).astype(
            int)
        padding_left, padding_right = 0, 0
    elif aspect < 1:
        new_height = conv_height
        new_width = numpy.round(new_height * aspect).astype(int)
        padding_horizontal = (conv_width - new_width) / 2
        padding_left, padding_right = numpy.floor(padding_horizontal).astype(int), numpy.ceil(
            padding_horizontal).astype(int)
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
