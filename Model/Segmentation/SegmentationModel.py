import numpy
import pydicom
import threading

from Controller.Segmentation.SegmentationListenerCode import SegmentationListenerCode
from typing import Callable, Tuple

from Model.Base import Utils
from Model.Base.SelectedFile import SelectedFile
from Model.Segmentation.Algorithms.Configuration.SegmentationAlgorithm import SegmentationAlgorithm
from Model.Segmentation.Algorithms.Configuration.SegmentationConfiguration import SegmentationConfiguration
from Model.Segmentation.Algorithms.Isocontour import isocontour_segment_image
from Model.Segmentation.Algorithms.Watershed import watershed_segment_image


class SegmentationModel(threading.Thread):

    def __init__(self, listener: Callable):
        threading.Thread.__init__(self)

        self.__listener = listener

        self.__selected_file: SelectedFile = None

    def load_dicom_image(self, file: SelectedFile):
        """
        Loads a DICOM image from the selected path.

        Args:
            path: A string, representing the path of the selected file.
        """
        self.__selected_file = file
        self.__selected_file.read()

        self.__listener(SegmentationListenerCode.DID_LOAD_IMAGE,
                        image=Utils.resize_image(image=self.__selected_file.image_tensor[:, :, 0],
                                                 size=(400, 400),
                                                 background_color=127),
                        z_axis_limit=self.get_range(2),
                        tensor_range=(numpy.amin(self.__selected_file.image_tensor),
                                      numpy.amax(self.__selected_file.image_tensor))
                        )

    def segment_image(self, image, configuration: SegmentationConfiguration):
        if configuration.get_algorithm() == SegmentationAlgorithm.ISOCONTOUR:
            upper_threshold = configuration.get_configuration()['upper_threshold']
            lower_threshold = configuration.get_configuration()['lower_threshold']
            return isocontour_segment_image(image, upper_threshold, lower_threshold)

        elif configuration.get_algorithm() == SegmentationAlgorithm.WATERSHED:
            threshold = configuration.get_configuration()['threshold']
            return watershed_segment_image(image, threshold)

    def get_range(self, axis: int):
        """
        Returns the range of the DICOM file in a certain axis.

        Args:
            axis: An intener, representing the axis.

        Returns:
            An integer, representing the range of the DICOM file in a certain axis.
        """
        return self.__selected_file.image_tensor.shape[axis] - 1

    def get_slice_image(self, axis: int, slice_index: int) -> numpy.ndarray:
        """
        Returns the slide image in an axis with a certain index.

        Args:
            axis: An integer, representing the axis.
            slice_index: An integer, representing the index of the image in the axis.

        Returns:
            An image, represented as a numpy array.
        """
        if axis == 0:
            return Utils.resize_image(image=self.__selected_file.image_tensor[slice_index, :, :],
                                      size=(400, 400),
                                      background_color=127)
        elif axis == 1:
            return Utils.resize_image(image=self.__selected_file.image_tensor[:, slice_index, :],
                                      size=(400, 400),
                                      background_color=127)
        elif axis == 2:
            return Utils.resize_image(image=self.__selected_file.image_tensor[:, :, slice_index],
                                      size=(400, 400),
                                      background_color=127)
