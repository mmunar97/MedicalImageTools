import numpy
import tkinter as tk

from PIL import Image, ImageTk
from tkinter import messagebox
from typing import Callable, Tuple

from Controller.Registering.RegisteringListenerCode import RegisteringListenerCode
from View.Registering.Subviews.ReadDicomFiles import ReadDicomFiles
from View.Utils.Base import Base
from View.Registering.ViewBuilder import ToolsViewBuilder
from View.Utils.Values.Color import Color
from View.Utils.Values.Font import Font


class RegisterView(object):

    __tool_panel_background_color = "#999999"

    def __init__(self, root_view: tk.Tk, listener: Callable):
        self.__root_view = root_view
        self.__listener = listener

        self.__load_image_button_image = Base.create_image_from_path("View/Registering/Assets/open_file.png", shape=(40, 40))
        self.__load_images_button = Base.create_button(parent_view=self.__root_view,
                                                       text="   Read files   ",
                                                       position=(10, 10),
                                                       image=self.__load_image_button_image,
                                                       command=self.open_file_dialog)

        self.__separator_view = Base.create_separator(parent_view=self.__root_view,
                                                      background_color=Color.TOOLS_PANEL_BACKGROUND,
                                                      position=(0, 65),
                                                      size=(1300, 2))

        self.__waiting_image = Base.create_image_from_path("View/Registering/Assets/waiting.png")

        self.__first_image_view_image = self.__waiting_image
        self.__first_image_view, self.__first_associated_image_view = Base.create_image_view(
            parent_view=self.__root_view,
            image=self.__waiting_image,
            position=(25, 95),
            size=(300, 300))
        self.__second_image_view_image = self.__waiting_image
        self.__second_image_view, self.__second_associated_image_view = Base.create_image_view(
            parent_view=self.__root_view,
            image=self.__waiting_image,
            position=(25, 420),
            size=(300, 300))

        self.__alpha_image_view_image = self.__waiting_image
        self.__alpha_image_view, self.__alpha_associated_image_view = Base.create_image_view(
            parent_view=self.__root_view,
            image=self.__waiting_image,
            position=(350, 95),
            size=(300, 300))

        self.__registered_image_view_image = self.__waiting_image
        self.__registered_image_view, self.__registered_associated_image_view = Base.create_image_view(
            parent_view=self.__root_view,
            image=self.__registered_image_view_image,
            position=(350, 420),
            size=(300, 300)
        )

        self.__tools_container = Base.create_container(
            parent_view=self.__root_view,
            background_color=Color.TOOLS_PANEL_BACKGROUND,
            position=(750, 0),
            size=(350, 750)
        )

        self.__slices_control_label = Base.create_text_view(
            parent_view=self.__root_view,
            background_color=Color.TOOLS_PANEL_BACKGROUND,
            text="SLICE CONTROL",
            font=Font.BOLD,
            position=(770, 30)
        )
        self.__axis_radio_button_group_value = Base.create_integer_variable()
        self.__radio_button_x_axis, self.__radio_button_y_axis, self.__radio_button_z_axis = ToolsViewBuilder.create_radio_button_group_slices(
            parent_view=self.__root_view,
            variable=self.__axis_radio_button_group_value,
            command=self.radio_button_did_change
        )

        self.__slice_slider_value = Base.create_integer_variable()
        self.__slice_slider = Base.create_slider(
            parent_view=self.__root_view,
            range=(0, 100),
            orientation=tk.HORIZONTAL,
            background_color=Color.TOOLS_PANEL_BACKGROUND,
            variable=self.__slice_slider_value,
            command=self.slice_slider_did_change,
            position=(780, 100),
            length=270,
            enabled=False
        )

        self.__separator_view_1 = Base.create_separator(
            parent_view=self.__root_view,
            background_color=Color.TOOLS_PANEL_SEPARATOR,
            position=(750, 160),
            size=(350, 2)
        )

        self.__alpha_control_label = Base.create_text_view(
            parent_view=self.__root_view,
            background_color=Color.TOOLS_PANEL_BACKGROUND,
            text="ALPHA",
            font=Font.BOLD,
            position=(770, 170)
        )
        self.__alpha_slider_value = Base.create_integer_variable()
        self.__alpha_slider = Base.create_slider(
            parent_view=self.__root_view,
            range=(0, 100),
            orientation=tk.HORIZONTAL,
            background_color=Color.TOOLS_PANEL_BACKGROUND,
            variable=self.__alpha_slider_value,
            command=self.alpha_slider_did_change,
            position=(780, 190),
            length=270,
            enabled=False
        )

        self.__separator_view_2 = Base.create_separator(
            parent_view=self.__root_view,
            background_color=Color.TOOLS_PANEL_SEPARATOR,
            position=(750, 250),
            size=(350, 2)
        )

        self.__registering_control_label = Base.create_text_view(
            parent_view=self.__root_view,
            background_color=Color.TOOLS_PANEL_BACKGROUND,
            text="REGISTERING",
            font=Font.BOLD,
            position=(770, 260)
        )

        self.__optimizer_parameters_control_label = Base.create_text_view(
            parent_view=self.__root_view,
            background_color=Color.TOOLS_PANEL_BACKGROUND,
            text="OPTIMIZER PARAMETERS",
            font=Font.REGULAR,
            position=(780, 290)
        )

        self.__optimizer_parameters_learning_rate_label = Base.create_text_view(
            parent_view=self.__root_view,
            background_color=Color.TOOLS_PANEL_BACKGROUND,
            text="Learning rate",
            font=Font.REGULAR,
            position=(790, 320)
        )

        self.__optimizer_parameters_learning_rate_entry = Base.create_edit_text(
            parent_view=self.__root_view,
            position=(940, 320),
            size=(110, 20)
        )

        self.__optimizer_parameters_iterations_label = Base.create_text_view(
            parent_view=self.__root_view,
            background_color=Color.TOOLS_PANEL_BACKGROUND,
            text="Number iterations",
            font=Font.REGULAR,
            position=(790, 350)
        )

        self.__optimizer_parameters_iterations_entry = Base.create_edit_text(
            parent_view=self.__root_view,
            position=(940, 350),
            size=(110, 20)
        )

        self.__similarity_control_label = Base.create_text_view(
            parent_view=self.__root_view,
            background_color=Color.TOOLS_PANEL_BACKGROUND,
            text="SIMILARITY FUNCTION (Mutual information)",
            font=Font.REGULAR,
            position=(780, 380)
        )

        self.__similarity_number_bins_label = Base.create_text_view(
            parent_view=self.__root_view,
            background_color=Color.TOOLS_PANEL_BACKGROUND,
            text="Number bins",
            font=Font.REGULAR,
            position=(790, 410)
        )

        self.__similarity_number_bins_entry = Base.create_edit_text(
            parent_view=self.__root_view,
            position=(940, 410),
            size=(110, 20)
        )

        self.__compute_registration_button = Base.create_button(
            parent_view=self.__root_view,
            text="Compute registration",
            position=(870, 450),
            command=self.start_registration
        )

    def enable_widgets(self):
        """
        Enables all the widgets in the view.
        """
        self.__axis_radio_button_group_value.set(0)
        self.__radio_button_x_axis.configure(state='active')
        self.__radio_button_y_axis.configure(state='active')
        self.__radio_button_z_axis.configure(state='active')
        self.__slice_slider.configure(state='active')
        self.__alpha_slider.configure(state='active')
        self.__alpha_slider_value.set(100)

    def set_slider_limit(self, lower_limit: int, upper_limit: int):
        """
        Sets the limit in the slice slider.

        Args:
            lower_limit: An integer, representing the lower limit.
            upper_limit: An integer, representing the upper limit.

        """
        self.__slice_slider.configure(from_=lower_limit, to=upper_limit, state='active')

    def radio_button_did_change(self):
        """
        Detects an action in the slice radio button group and notifies the controller the action.
        """
        self.__slice_slider_value.set(0)
        self.__alpha_slider_value.set(100)
        self.__listener(RegisteringListenerCode.RADIO_BUTTON_CHANGED, axis=self.__axis_radio_button_group_value.get())

    def slice_slider_did_change(self, _):
        """
        Detects that the slice slider has changed its value.
        """
        self.__listener(RegisteringListenerCode.SLICE_SLIDER_CHANGED,
                        axis=self.__axis_radio_button_group_value.get(),
                        slice=self.__slice_slider_value.get(),
                        alpha=self.__alpha_slider_value.get())

    def alpha_slider_did_change(self, _):
        """
        Detects that the alpha slider has changed its value.
        """
        self.__listener(RegisteringListenerCode.ALPHA_SLIDER_CHANGED,
                        axis=self.__axis_radio_button_group_value.get(),
                        slice=self.__slice_slider_value.get(),
                        alpha=self.__alpha_slider_value.get())

    def set_images(self, image1: numpy.ndarray, image2: numpy.ndarray,
                   alpha_image: numpy.ndarray, registered_image: numpy.ndarray=None):
        """
        Sets the received images.

        Args:
            image1: An image to be shown, represented as a numpy array.
            image2: An image to be shown, represented as a numpy array.
            alpha_image: The alpha-combination of both images, represented as a numpy array.
            registered_image: The registered image, represented as a numpy array.
        """
        self.__first_image_view_image = ImageTk.PhotoImage(image=Image.fromarray(image1))
        self.__first_image_view.itemconfig(self.__first_associated_image_view, image=self.__first_image_view_image)

        self.__second_image_view_image = ImageTk.PhotoImage(image=Image.fromarray(image2))
        self.__second_image_view.itemconfig(self.__second_associated_image_view, image=self.__second_image_view_image)

        self.__alpha_image_view_image = ImageTk.PhotoImage(image=Image.fromarray(alpha_image))
        self.__alpha_image_view.itemconfig(self.__alpha_associated_image_view, image=self.__alpha_image_view_image)

        if registered_image is not None:
            self.__registered_image_view_image = ImageTk.PhotoImage(image=Image.fromarray(registered_image))
            self.__registered_image_view.itemconfig(self.__registered_associated_image_view,
                                                    image=self.__registered_image_view_image)

        self.__root_view.update()

    def open_file_dialog(self):
        """
        Opens the window that allows to pick the files to be opened.
        """
        window = tk.Toplevel()
        window.resizable(False, False)
        window.geometry("490x260+30+70")

        _ = ReadDicomFiles(window, self.__listener)

    def start_registration(self):
        """
        Starts the registering process.
        """

        learning_rate = float(self.__optimizer_parameters_learning_rate_entry.get())
        number_iterations = int(self.__optimizer_parameters_iterations_entry.get())
        number_bins = int(self.__similarity_number_bins_entry.get())

        self.__listener(RegisteringListenerCode.REGISTERING_WILL_START,
                        learning_rate=learning_rate,
                        number_iterations=number_iterations,
                        number_bins=number_bins)
        try:
            pass
        except:
            messagebox.showerror("Error in parameters", "Some of the introduced parameters are not correct.")


    @staticmethod
    def end_registration():
        """
        Shows an alert indicating that the registration process has finished.
        """
        messagebox.showerror("Registration completed", "The images have been registered successfully.")


    @staticmethod
    def show_read_status(status: int):
        """
        Shows a dialog with the status of the reading process.
        Args:
            status: An integer, representing the status of the reading process. 1 represents success and -1
                    represents error.
        """
        if status == 1:
            messagebox.showerror("Read success", "The images have been loaded successfully.")
        elif status == -1:
            messagebox.showerror("Error while reading", "Some error has occurred while reading the files.")


def show_main_view(listener: Callable) -> Tuple[tk.Tk, RegisterView]:
    """
    Initializes the main view.

    Args:
        listener: The callable method that acts as listener of the execution.

    Returns:
        A tuple of two tkinter objects: the root view and the main view.
    """
    root_view = tk.Tk()
    root_view.resizable(False, False)
    root_view.title('Medical Image Registration')

    main_view = RegisterView(root_view, listener)
    root_view.geometry("1100x750+10+10")

    return root_view, main_view
