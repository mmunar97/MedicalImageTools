from Controller.Main.MainListenerCode import MainListenerCode
from Controller.Main.WelcomeController import WelcomeController
from Controller.Registering.RegisteringController import RegisteringController
from Controller.Segmentation.SegmentationController import SegmentationController


class GlobalController:

    def __init__(self):

        self.__selected_mode: MainListenerCode = None

        WelcomeController(self.set_selected_mode)
        if self.__selected_mode == MainListenerCode.SEGMENTATION_SELECTED:
            SegmentationController()
        elif self.__selected_mode == MainListenerCode.REGISTERING_SELECTED:
            RegisteringController()

    def set_selected_mode(self, action_code: MainListenerCode):
        self.__selected_mode = action_code
