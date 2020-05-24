import numpy
import tkinter as tk

from Controller.Segmentation.SegmentationListenerCode import SegmentationListenerCode
from PIL import Image, ImageTk
from typing import Callable, Tuple

from Model.Segmentation.Algorithms.Configuration.SegmentationAlgorithm import SegmentationAlgorithm
from Model.Segmentation.Algorithms.Configuration.SegmentationConfiguration import SegmentationConfiguration
from View.Segmentation.Subviews.ReadDicomFiles import ReadDicomFiles
from View.Segmentation.ViewBuilder import ToolsViewBuilder
from View.Utils.Base import Base
from View.Utils.Values.Color import Color
from View.Utils.Values.Font import Font


class SegmentationView(object):

    def __init__(self, root_view: tk.Tk, listener: Callable):

        self.__root_view = root_view
        self.__listener = listener

        # region Tools top bar
        self.__load_image_button_image = Base.create_image_from_path("View/Segmentation/Assets/open_file.png",
                                                                     shape=(40, 40))
        self.__load_images_button = Base.create_button(parent_view=self.__root_view,
                                                       text="   Read file   ",
                                                       position=(10, 10),
                                                       image=self.__load_image_button_image,
                                                       command=self.open_file_dialog)

        self.__menu_separator_view = Base.create_separator(parent_view=self.__root_view,
                                                           background_color=Color.TOOLS_PANEL_BACKGROUND,
                                                           position=(0, 65),
                                                           size=(1300, 2))
        # endregion

        # region Image views
        self.__waiting_image = Base.create_image_from_path("View/Segmentation/Assets/waiting.png")

        self.__image_view_image = self.__waiting_image
        self.__image_view, self.__associated_image_view = Base.create_image_view(
            parent_view=self.__root_view,
            image=self.__image_view_image,
            position=(25, 90),
            size=(400, 400))

        self.__segmented_mask_image = self.__waiting_image
        self.__segmented_mask_image_view, self.__associated_segmented_mask_image_view = Base.create_image_view(
            parent_view=self.__root_view,
            image=self.__segmented_mask_image,
            position=(450, 90),
            size=(400, 400)
        )

        self.__segmented_image = self.__waiting_image
        self.__segmented_image_view, self.__associated_segmented_image_view = Base.create_image_view(
            parent_view=self.__root_view,
            image=self.__segmented_image,
            position=(875, 90),
            size=(400, 400)
        )
        # endregion

        self.__tools_container = Base.create_container(
            parent_view=self.__root_view,
            background_color=Color.TOOLS_PANEL_BACKGROUND,
            position=(0, 520),
            size=(1300, 430)
        )

        self.__slices_control_label = Base.create_text_view(
            parent_view=self.__root_view,
            background_color=Color.TOOLS_PANEL_BACKGROUND,
            text="SLICE CONTROL",
            font=Font.BOLD,
            position=(40, 550)
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
            position=(50, 620),
            length=270,
            enabled=False
        )

        self.__tools_1_separator_view = Base.create_separator(
            parent_view=self.__root_view,
            background_color=Color.TOOLS_PANEL_SEPARATOR,
            position=(350, 520),
            size=(2, 430)
        )

        self.__segmentation_mode_label = Base.create_text_view(
            parent_view=self.__root_view,
            background_color=Color.TOOLS_PANEL_BACKGROUND,
            text="SEGMENTATION MODE",
            font=Font.BOLD,
            position=(370, 550)
        )

        self.__segmentation_mode_group_value = Base.create_integer_variable()
        self.__isocontour_radio_button, self.__watershed_radio_button = ToolsViewBuilder.create_radio_button_group_segmentation_mode(
            parent_view=self.__root_view,
            variable=self.__segmentation_mode_group_value,
            command=self.segmentation_radio_button_did_change
        )

        self.__tools_2_separator_view = Base.create_separator(
            parent_view=self.__root_view,
            background_color=Color.TOOLS_PANEL_SEPARATOR,
            position=(560, 520),
            size=(2, 430)
        )

        self.__isocontour_parameters_label = Base.create_text_view(
            parent_view=self.__root_view,
            background_color=Color.TOOLS_PANEL_BACKGROUND,
            text="ISOCONTOUR PARAMETERS",
            font=Font.BOLD,
            position=(580, 550)
        )

        self.__isocontour_threshold_label = Base.create_text_view(
            parent_view=self.__root_view,
            background_color=Color.TOOLS_PANEL_BACKGROUND,
            text="Upper and lower threshold:",
            font=Font.REGULAR,
            position=(590, 570)
        )

        self.__isocontour_upper_threshold_slider_value = Base.create_integer_variable()
        self.__isocontour_upper_threshold_slider = Base.create_slider(
            parent_view=self.__root_view,
            range=(0, 100),
            orientation=tk.HORIZONTAL,
            background_color=Color.TOOLS_PANEL_BACKGROUND,
            variable=self.__isocontour_upper_threshold_slider_value,
            command=self.isocontour_slider_did_change,
            position=(590, 590),
            length=230,
            enabled=False
        )

        self.__isocontour_lower_threshold_slider_value = Base.create_integer_variable()
        self.__isocontour_lower_threshold_slider = Base.create_slider(
            parent_view=self.__root_view,
            range=(0, 100),
            orientation=tk.HORIZONTAL,
            background_color=Color.TOOLS_PANEL_BACKGROUND,
            variable=self.__isocontour_lower_threshold_slider_value,
            command=self.isocontour_slider_did_change,
            position=(590, 640),
            length=230,
            enabled=False
        )

        self.__tools_3_separator_view = Base.create_separator(
            parent_view=self.__root_view,
            background_color=Color.TOOLS_PANEL_SEPARATOR,
            position=(850, 520),
            size=(2, 430)
        )

        self.__watershed_parameters_label = Base.create_text_view(
            parent_view=self.__root_view,
            background_color=Color.TOOLS_PANEL_BACKGROUND,
            text="WATERSHED PARAMETERS",
            font=Font.BOLD,
            position=(870, 550)
        )

        self.__watershed_threshold_slider_value = Base.create_integer_variable()
        self.__watershed_threshold_slider = Base.create_slider(
            parent_view=self.__root_view,
            range=(0, 100),
            orientation=tk.HORIZONTAL,
            background_color=Color.TOOLS_PANEL_BACKGROUND,
            variable=self.__watershed_threshold_slider_value,
            command=self.watershed_slider_did_change,
            position=(880, 600),
            length=230,
            enabled=False
        )

    def open_file_dialog(self):
        """
        Opens a file dialog requesting the user the path of the DICOM file to be opened.
        """
        window = tk.Toplevel()
        window.resizable(False, False)
        window.geometry("490x200+30+70")

        _ = ReadDicomFiles(window, self.__listener)

    def radio_button_did_change(self):
        """
        Detects an action in the slice radio button group and notifies the controller the action.
        """
        self.__listener(SegmentationListenerCode.AXIS_DID_CHANGE,
                        axis=self.__axis_radio_button_group_value.get())
        self.__slice_slider_value.set(0)
        self.compute_image()

    def slice_slider_did_change(self, _):
        """
        Detects that the slice slider has changed its value.
        """
        self.compute_image()

    def segmentation_radio_button_did_change(self):
        """
        Detects an action in the segmentation mode radio group and notifies the controller the action.
        """
        if self.__segmentation_mode_group_value.get() == 0:
            self.__isocontour_upper_threshold_slider.configure(state='active')
            self.__isocontour_lower_threshold_slider.configure(state='active')
            self.__watershed_threshold_slider.configure(state='disabled')
        elif self.__segmentation_mode_group_value.get() == 1:
            self.__isocontour_upper_threshold_slider.configure(state='disabled')
            self.__isocontour_lower_threshold_slider.configure(state='disabled')
            self.__watershed_threshold_slider.configure(state='active')

        self.__segmented_image_view.itemconfig(self.__associated_segmented_image_view,
                                               image=self.__waiting_image)
        self.__segmented_mask_image_view.itemconfig(self.__associated_segmented_mask_image_view,
                                                    image=self.__waiting_image)
        self.__root_view.update()

    def isocontour_slider_did_change(self, _):
        """
        Detects that the isocontour threshold slider has changed its value.
        """
        self.compute_image()

    def watershed_slider_did_change(self, _):
        """
        Detects that the watershed threshold slider has changed its value.
        """
        self.compute_image()

    def compute_image(self):
        """
        Queries the controller the new image from the settings.
        """
        configuration: SegmentationConfiguration = None
        if self.__segmentation_mode_group_value.get() == 0:
            configuration = SegmentationConfiguration(algorithm=SegmentationAlgorithm.ISOCONTOUR,
                                                      configuration={'upper_threshold': self.__isocontour_upper_threshold_slider_value.get(),
                                                                     'lower_threshold': self.__isocontour_lower_threshold_slider_value.get()})
        elif self.__segmentation_mode_group_value.get() == 1:
            configuration = SegmentationConfiguration(algorithm=SegmentationAlgorithm.WATERSHED,
                                                      configuration={'threshold': self.__watershed_threshold_slider.get()})

        self.__listener(SegmentationListenerCode.VISUALIZATION_PARAMETERS_DID_CHANGE,
                        axis=self.__axis_radio_button_group_value.get(),
                        slice=self.__slice_slider_value.get(),
                        segmentation_settings=configuration)

    def enable_widgets(self):
        """
        Enables all the widgets in the view.
        """
        self.__axis_radio_button_group_value.set(0)
        self.__radio_button_x_axis.configure(state='active')
        self.__radio_button_y_axis.configure(state='active')
        self.__radio_button_z_axis.configure(state='active')
        self.__slice_slider.configure(state='active')

        self.__isocontour_radio_button.configure(state='active')
        self.__watershed_radio_button.configure(state='active')

        self.__isocontour_upper_threshold_slider.configure(state='active')
        self.__isocontour_lower_threshold_slider.configure(state='active')

    def set_slider_limit(self, lower_limit: int, upper_limit: int):
        """
        Sets the limit in the slice slider.

        Args:
            lower_limit: An integer, representing the lower limit.
            upper_limit: An integer, representing the upper limit.
        """
        self.__slice_slider.configure(from_=lower_limit, to=upper_limit, state='active')

    def set_segmentation_methods_slider_limit(self, lower_limit: int, upper_limit: int):
        """
        Sets the limit in the isocontour threshold slider.
        Args:
            lower_limit: An integer, representing the lower limit.
            upper_limit: An integer, representing the upper limit.
        """
        self.__isocontour_upper_threshold_slider.configure(from_=lower_limit, to=upper_limit, state='active')
        self.__isocontour_lower_threshold_slider.configure(from_=lower_limit, to=upper_limit, state='active')

        self.__isocontour_upper_threshold_slider_value.set(upper_limit)
        self.__isocontour_lower_threshold_slider_value.set(lower_limit)

        self.__watershed_threshold_slider.configure(from_=lower_limit, to=upper_limit, state='active')

    def set_images(self, original_image: numpy.ndarray, mask_image: numpy.ndarray=None, marked_image: numpy.ndarray=None):
        """
        Sets the image in the ImageView.

        Args:
            original_image: The image to be shown, represented as a numpy array.
        """
        self.__image_view_image = ImageTk.PhotoImage(image=Image.fromarray(original_image))
        self.__image_view.itemconfig(self.__associated_image_view, image=self.__image_view_image)

        if mask_image is not None:
            self.__segmented_mask_image = ImageTk.PhotoImage(image=Image.fromarray(mask_image))
            self.__segmented_mask_image_view.itemconfig(self.__associated_segmented_mask_image_view,
                                                        image=self.__segmented_mask_image)
        if marked_image is not None:
            self.__segmented_image = ImageTk.PhotoImage(image=Image.fromarray(marked_image))
            self.__segmented_image_view.itemconfig(self.__associated_segmented_image_view,
                                                   image=self.__segmented_image)

        self.__root_view.update()


def show_main_view(listener: Callable) -> Tuple[tk.Tk, SegmentationView]:
    """
    Initializes the main view.

    Args:
        listener: The callable method that acts as listener of the execution.

    Returns:
        A tuple of two tkinter objects: the root view and the main view.
    """
    root_view = tk.Tk()
    root_view.resizable(False, False)
    root_view.title('Medical Image Segmentation')

    main_view = SegmentationView(root_view, listener)
    root_view.geometry("1300x690+10+10")

    return root_view, main_view
