from enum import Enum


class SegmentationListenerCode(Enum):
    DID_PICKED_IMAGE = 0
    DID_LOAD_IMAGE = 1
    VISUALIZATION_PARAMETERS_DID_CHANGE = 2
    AXIS_DID_CHANGE = 3


