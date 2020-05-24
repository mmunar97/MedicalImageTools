import tkinter as tk
from typing import Callable, Tuple

from Controller.Main.MainListenerCode import MainListenerCode
from View.Utils.Base import Base
from View.Utils.Values.Color import Color
from View.Utils.Values.Font import Font


class WelcomeView(object):

    def __init__(self, root_view: tk.Tk, listener: Callable):
        self.__root_view = root_view
        self.__listener = listener

        self.__application_title_text_view = Base.create_text_view(parent_view=self.__root_view,
                                                                   text="Medical Image Tools",
                                                                   background_color=Color.CLEAR_BACKGROUND,
                                                                   font=Font.TITLE_BOLD,
                                                                   position=(20, 20))
        self.__author_title_text_view = Base.create_text_view(parent_view=self.__root_view,
                                                              text="Marc Munar Covas (marc.munar@uib.es)",
                                                              background_color=Color.CLEAR_BACKGROUND,
                                                              font=Font.REGULAR,
                                                              position=(20, 50))
        self.__institution_title_text_view = Base.create_text_view(parent_view=self.__root_view,
                                                                   text="Medical Image Processing – Universitat de les Illes Balears",
                                                                   background_color=Color.CLEAR_BACKGROUND,
                                                                   font=Font.REGULAR,
                                                                   position=(20, 80))

        self.__start_segmentation_button = Base.create_button(parent_view=self.__root_view,
                                                              text="   Segmentation tools   ",
                                                              position=(20, 140),
                                                              command=self.start_segmentation)

        self.__start_registering_button = Base.create_button(parent_view=self.__root_view,
                                                             text="   Registering tools   ",
                                                             position=(20, 180),
                                                             command=self.start_registering)

    def start_segmentation(self):
        self.__listener(MainListenerCode.SEGMENTATION_SELECTED)

    def start_registering(self):
        self.__listener(MainListenerCode.REGISTERING_SELECTED)


def show_main_view(listener: Callable) -> Tuple[tk.Tk, WelcomeView]:
    """
    Initializes the welcome view.

    Args:
        listener: The callable method that acts as listener of the execution.

    Returns:
        A tuple of two tkinter objects: the root view and the main view.
    """
    root_view = tk.Tk()
    root_view.resizable(False, False)
    root_view.title('Medical Image Tools')

    main_view = WelcomeView(root_view, listener)
    root_view.geometry("420x250+200+200")

    return root_view, main_view
