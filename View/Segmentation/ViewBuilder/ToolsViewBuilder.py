import tkinter as tk
from typing import Callable, Tuple

from View.Utils.Base import Base
from View.Utils.Values.Color import Color


def create_radio_button_group_slices(parent_view: tk.BaseWidget,
                                     variable: tk.IntVar,
                                     command: Callable) -> Tuple[tk.Radiobutton, tk.Radiobutton, tk.Radiobutton]:
    """
    Creates the radio button group for the axis selection in the axis view.

    Args:
        parent_view: A Tk object, representing the root view.
        variable: A IntVar object, representing the variable that stores the value of the selected button.
        command: A Callable method, representing the action to handle if a button has changed.

    Returns:
        A group of three RadioButton.
    """
    separation = 80
    x_axis_radio_button = Base.create_radio_button(parent_view,
                                                   text="X axis",
                                                   background_color=Color.TOOLS_PANEL_BACKGROUND,
                                                   variable=variable,
                                                   assigned_value=0,
                                                   command=command,
                                                   position=(50+0*separation, 590),
                                                   enabled=False)
    y_axis_radio_button = Base.create_radio_button(parent_view,
                                                   text="Y axis",
                                                   background_color=Color.TOOLS_PANEL_BACKGROUND,
                                                   variable=variable,
                                                   assigned_value=1,
                                                   command=command,
                                                   position=(50+separation, 590),
                                                   enabled=False)

    z_axis_radio_button = Base.create_radio_button(parent_view,
                                                   text="Z axis",
                                                   background_color=Color.TOOLS_PANEL_BACKGROUND,
                                                   variable=variable,
                                                   assigned_value=2,
                                                   command=command,
                                                   position=(50+2*separation, 590),
                                                   enabled=False)

    return x_axis_radio_button, y_axis_radio_button, z_axis_radio_button


def create_radio_button_group_segmentation_mode(parent_view: tk.BaseWidget,
                                                variable: tk.IntVar,
                                                command: Callable) -> Tuple[tk.Radiobutton, tk.Radiobutton]:
    """
    Creates the radio button group for the segmentation algorithm selection.

    Args:
        parent_view: A Tk object, representing the root view.
        variable: A IntVar object, representing the variable that stores the value of the selected button.
        command: A Callable method, representing the action to handle if a button has changed.

    Returns:
        A group of two RadioButton.
    """
    separation = 30
    isocontour_radio_button = Base.create_radio_button(parent_view,
                                                       text="Isocontour",
                                                       background_color=Color.TOOLS_PANEL_BACKGROUND,
                                                       variable=variable,
                                                       assigned_value=0,
                                                       command=command,
                                                       position=(380, 600+0*separation),
                                                       enabled=False)
    watershed_radio_button = Base.create_radio_button(parent_view,
                                                      text="Watershed",
                                                      background_color=Color.TOOLS_PANEL_BACKGROUND,
                                                      variable=variable,
                                                      assigned_value=1,
                                                      command=command,
                                                      position=(380, 600+1*separation),
                                                      enabled=False)
    return isocontour_radio_button, watershed_radio_button
