from Model.Segmentation.Algorithms.Configuration.SegmentationAlgorithm import SegmentationAlgorithm
from typing import Dict


class SegmentationConfiguration:

    def __init__(self, algorithm: SegmentationAlgorithm, configuration: Dict):
        self.__algorithm = algorithm
        self.__configuration = configuration

    def get_algorithm(self):
        return self.__algorithm

    def get_configuration(self):
        return self.__configuration
