import cv2
import matplotlib.cm as cm
import numpy
import SimpleITK as itk
import threading

from typing import Callable, Tuple

from Controller.Registering.RegisteringListenerCode import RegisteringListenerCode
from Model.Base import Utils
from Model.Base.SelectedFile import SelectedFile


class RegisteringModel(threading.Thread):

    def __init__(self, listener: Callable):
        threading.Thread.__init__(self)

        self.__listener = listener

        self.__first_image_file: SelectedFile = None
        self.__second_image_file: SelectedFile = None
        self.__registered_images: numpy.ndarray = None

    def set_picked_files(self, first_image_file: SelectedFile, second_image_file: SelectedFile):
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

            self.__listener(RegisteringListenerCode.IMAGES_READ, status=1,
                            upper_limit=self.get_tensor_limit_for_axis(0))
        except Exception:
            self.__listener(RegisteringListenerCode.IMAGES_READ, status=-1)

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
                          alpha: int) -> Tuple[numpy.ndarray, numpy.ndarray, numpy.ndarray, numpy.ndarray]:
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
        registered: numpy.ndarray = None

        # The result of registration has the same shape as __first_image_file, since this image is considered
        # as ground truth.

        if axis == 0:
            image1 = self.__first_image_file.image_tensor[min(slice, image1_limit - 1), :, :]
            image2 = self.__second_image_file.image_tensor[min(slice, image2_limit - 1), :, :]

            if self.__registered_images is not None:
                registered = self.__registered_images[min(slice, image1_limit - 1), :, :]
        elif axis == 1:
            image1 = self.__first_image_file.image_tensor[:, min(slice, image1_limit - 1), :]
            image2 = self.__second_image_file.image_tensor[:, min(slice, image2_limit - 1), :]

            if self.__registered_images is not None:
                registered = self.__registered_images[:, min(slice, image1_limit - 1), :]
        elif axis == 2:
            image1 = self.__first_image_file.image_tensor[:, :, min(slice, image1_limit - 1)]
            image2 = self.__second_image_file.image_tensor[:, :, min(slice, image2_limit - 1)]

            if self.__registered_images is not None:
                registered = self.__registered_images[:, :, min(slice, image1_limit - 1)]

        image1 = Utils.resize_image(image1, size=(300, 300), background_color=127)
        image2 = Utils.resize_image(image2, size=(300, 300), background_color=127)

        if self.__registered_images is not None:
            registered = Utils.resize_image(registered, size=(300, 300), background_color=127)

        alpha_image = (1 - alpha / 100) * image1 + (alpha / 100) * image2

        return image1, image2, alpha_image, registered

    def register_images(self, **kwargs):
        """
        Registers the images.
        """
        learning_rate = kwargs['learning_rate']
        number_iterations = kwargs['number_iterations']
        similarity_function = kwargs['similarity_function']

        img1 = itk.GetImageFromArray(self.__first_image_file.image_tensor.astype(numpy.float32))
        img2 = itk.GetImageFromArray(self.__second_image_file.image_tensor.astype(numpy.float32))

        registration_method = itk.ImageRegistrationMethod()

        if similarity_function == 0:
            registration_method.SetMetricAsCorrelation()
        elif similarity_function == 1:
            registration_method.SetMetricAsMeanSquares()

        registration_method.SetMetricSamplingStrategy(registration_method.RANDOM)
        registration_method.SetMetricSamplingPercentage(0.01)

        registration_method.SetInterpolator(itk.sitkLinear)
        registration_method.SmoothingSigmasAreSpecifiedInPhysicalUnitsOn()

        registration_method.SetOptimizerAsGradientDescent(learningRate=learning_rate,
                                                          numberOfIterations=number_iterations,
                                                          convergenceMinimumValue=1e-6, convergenceWindowSize=10)

        initial_transform = itk.CenteredTransformInitializer(img1,
                                                             img2,
                                                             itk.Euler3DTransform(),
                                                             itk.CenteredTransformInitializerFilter.GEOMETRY)

        registration_method.SetInitialTransform(initial_transform, inPlace=False)
        final_transform = registration_method.Execute(img1, img2)

        resampler = itk.ResampleImageFilter()
        resampler.SetReferenceImage(img2)
        resampler.SetInterpolator(itk.sitkLinear)
        resampler.SetDefaultPixelValue(100)
        resampler.SetTransform(final_transform)

        out = resampler.Execute(img2)

        print('Final metric value: {0}'.format(registration_method.GetMetricValue()))
        print('Optimizer\'s stopping condition, {0}'.format(registration_method.GetOptimizerStopConditionDescription()))

        self.__registered_images = itk.GetArrayFromImage(out)
        self.__listener(RegisteringListenerCode.REGISTERING_DID_FINISH)


    def get_first_file(self):
        return self.__first_image_file

    def get_second_file(self):
        return self.__second_image_file

    def get_registered_images(self):
        return self.__registered_images
