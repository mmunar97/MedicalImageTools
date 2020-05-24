from Controller.Main.MainListenerCode import MainListenerCode
from typing import Callable
from View.Main import MainGUI


class WelcomeController:

    def __init__(self, listener: Callable):

        self.__listener = listener

        self.__root_view, self.__view = MainGUI.show_main_view(self.controller_listener)
        self.__root_view.mainloop()

    def controller_listener(self, action_code: MainListenerCode):
        self.__listener(action_code)
        self.__root_view.destroy()
