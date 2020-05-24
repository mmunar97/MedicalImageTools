import tkinter as tk

from PIL import Image, ImageTk
from typing import Any, Callable, Tuple

from View.Utils.Values.Color import Color
from View.Utils.Values.Font import Font


def create_image_from_path(path: str, shape=None) -> ImageTk.PhotoImage:
    """
    Reads an image and returns it as a PhotoImage object to be used in the buttons.

    Args:
        path: A string, representing the path of the image.
        shape: A tuple, representing the new size of the image (optional).

    Returns:
        A PhotoImage object, representing the read image.
    """
    if shape is not None:
        image = ImageTk.PhotoImage(Image.open(path).resize(shape, Image.BICUBIC))
    else:
        image = ImageTk.PhotoImage(Image.open(path))
    return image


def create_button(parent_view: tk.BaseWidget, text: str, position: Tuple[int, int], command: Callable = None,
                  image: ImageTk.PhotoImage = None) -> tk.Button:
    """
    Builds a button from its main components.

    Args:
        parent_view: A Tk object, representing the root view.
        text: A string, representing the text to be shown in the button.
        position: A Tuple of integers, representing the coordinates of the button.
        command: A Callable method, representing the action to be performed when the button is selected (optional).
        image: A PhotoImage object, representing the image to be shown in the button (optional).

    Returns:
        A Button object, representing the configured button.
    """

    assert len(position) == 2, "The coordinates must be a tuple with two integer components."
    if image is not None:
        button = tk.Button(parent_view,
                           text=text,
                           image=image,
                           compound="left",
                           command=command)
    else:
        button = tk.Button(parent_view,
                           text=text,
                           compound="left",
                           command=command)
    button.pack()
    button.place(x=position[0], y=position[1])

    return button


def create_image_view(parent_view: tk.Tk, image: ImageTk.PhotoImage, position: Tuple[int, int],
                      size: Tuple[int, int]) -> Tuple[tk.Canvas, Any]:
    """
    Creates a Canvas that shows an image.

    Args:
        parent_view: A Tk object, representing the root view.
        image: A PhotoImage object, representing the image to be shown in the canvas.
        position: A Tuple of integers, representing the coordinates of the canvas.
        size: A Tuple of integers, representing the shape of the view (width x height).

    Returns:
        A Canvas object, representing the view that contains the image.
    """
    image_view = tk.Canvas(parent_view, width=size[0], height=size[1])
    associated_image_view = image_view.create_image(0, 0, image=image, anchor=tk.NW)
    image_view.image = associated_image_view
    image_view.pack()
    image_view.place(x=position[0], y=position[1])

    return image_view, associated_image_view


def create_text_view(parent_view: tk.BaseWidget, text: str, background_color: Color,
                     font: Font, position: Tuple[int, int]) -> tk.Label:
    """
    Creates a label with text.

    Args:
        parent_view: A Tk object, representing the root view.
        text: The text to be shown.
        background_color: A Color object, representing the solid background color.
        font: The font to be used in the text.
        position: A Tuple of integers, representing the coordinates of the label.

    Returns:
        A Label object.
    """
    assert len(position) == 2, "The coordinates must be a tuple with two integer components."
    text_view = tk.Label(parent_view,
                         text=text,
                         font=font.value,
                         bg=background_color.value)
    text_view.pack()
    text_view.place(x=position[0], y=position[1])

    return text_view


def create_container(parent_view: tk.BaseWidget, background_color: Color,
                     position: Tuple[int, int], size: Tuple[int, int]) -> tk.Frame:
    """
    Creates a container.

    Args:
        parent_view: A Tk object, representing the root view.
        background_color: A Color object, representing the solid background color.
        position: A Tuple of integers, representing the coordinates of the container.
        size: A Tuple of integers, representing the shape of the view (width x height).

    Returns:
        A Frame object.
    """
    container = tk.Frame(parent_view, bg=background_color.value, width=size[0], height=size[1])
    container.place(x=position[0], y=position[1])

    return container


def create_integer_variable() -> tk.IntVar:
    """
    Creates a variable that stores the value of a group of radio buttons or a slider.

    Returns:
        A IntVar object.
    """
    return tk.IntVar()


def create_radio_button(parent_view: tk.BaseWidget, text: str, background_color: Color, variable: tk.IntVar,
                        assigned_value: int, command: Callable, position: Tuple[int, int],
                        enabled: bool) -> tk.Radiobutton:
    """
    Creates a radio button from its main components.

    Args:
        parent_view: A Tk object, representing the root view.
        text: The text to be shown in the button.
        background_color: A Color object, representing the solid background color.
        variable: A IntVar object, representing the variable that stores the value of the selected button
                  (if they form a group).
        assigned_value: An integer, representing the associated value to the button.
        command: A Callable method, representing the action to handle if a button has changed.
        position: A Tuple of integers, representing the coordinates of the container.
        enabled: A boolean, representing if the button is enabled or disabled.

    Returns:
        A RadioButton object.
    """
    radio_button = tk.Radiobutton(parent_view, text=text, bg=background_color.value, variable=variable,
                                  value=assigned_value, command=command)
    radio_button.pack()
    radio_button.place(x=position[0], y=position[1])

    if enabled:
        radio_button.configure(state='active')
    else:
        radio_button.configure(state='disabled')

    return radio_button


def create_slider(parent_view: tk.BaseWidget, range: Tuple[int, int], orientation: Any,
                  background_color: Color, variable: tk.IntVar, command: Callable, position: Tuple[int, int],
                  length: int, enabled: bool) -> tk.Scale:
    """
    Creates a slider from its main components.

    Args:
        parent_view: A Tk object, representing the root view.
        range: A tuple of integers, representing the range of sliding.
        orientation: A tk constant, representing if the orientation is vertical (tk.VERTICAL) or horizontal
                     (tk.HORIZONTAL).
        background_color: A Color object, representing the solid background color.
        variable: A IntVar object, representing the variable that stores the value of the selected button
                  (if they form a group).
        command: A Callable method, representing the action to handle if a button has changed.
        position: A Tuple of integers, representing the coordinates of the container.
        length: An integer, representing the length of the slider.
        enabled: A boolean, representing if the button is enabled or disabled.

    Returns:
        A Scale object.
    """
    slider = tk.Scale(parent_view,
                      from_=range[0], to=range[1],
                      orient=orientation,
                      bg=background_color.value,
                      variable=variable,
                      command=command,
                      length=length)

    slider.pack()
    slider.place(x=position[0], y=position[1])

    if enabled:
        slider.configure(state='active')
    else:
        slider.configure(state='disabled')
    return slider


def create_separator(parent_view: tk.BaseWidget, background_color: Color,
                     position: Tuple[int, int], size: Tuple[int, int]) -> tk.Frame:
    """
    Creates a separator.

    Args:
        parent_view: A Tk object, representing the root view.
        background_color: A Color object, representing the solid background color.
        position: A Tuple of integers, representing the coordinates of the container.
        size: A Tuple of integers, representing the shape of the view (width x height).

    Returns:
        A Frame object.
    """
    separator = tk.Frame(parent_view,
                         bg=background_color.value,
                         width=size[0],
                         height=size[1])
    separator.pack()
    separator.place(x=position[0], y=position[1])

    return separator


def create_edit_text(parent_view: tk.BaseWidget, position: Tuple[int, int], size: Tuple[int, int]) -> tk.Entry:
    """
    Creates a text for input.

    Args:
        parent_view: A Tk object, representing the root view.
        position: A Tuple of integers, representing the coordinates of the container.
        size: A Tuple of integers, representing the shape of the view (width x height).

    Returns:
        A Entry object.
    """
    entry = tk.Entry(parent_view)
    entry.pack()

    entry.place(x=position[0], y=position[1], width=size[0], height=size[1])

    return entry
