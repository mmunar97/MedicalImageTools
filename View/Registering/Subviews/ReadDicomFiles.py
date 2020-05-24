import tkinter as tk

from Controller.Registering.RegisteringListenerCode import RegisteringListenerCode
from Model.Base.SelectedFile import SelectedFile
from tkinter import filedialog
from tkinter import messagebox
from typing import Callable
from View.Utils.Base import Base
from View.Utils.Values.Font import Font
from View.Utils.Values.Color import Color


class ReadDicomFiles(object):

    def __init__(self, window: tk.Toplevel, listener: Callable):

        self.__root_window = window
        self.__listener = listener

        self.__first_image_file: SelectedFile = None
        self.__second_image_file: SelectedFile = None

        self.__title_label = Base.create_text_view(self.__root_window,
                                                   text="Select two DICOM files. Only DICOM files or folders are allowed.",
                                                   background_color=Color.CLEAR_BACKGROUND,
                                                   font=Font.REGULAR,
                                                   position=(20, 20))

        self.__first_image_title_label = Base.create_text_view(self.__root_window,
                                                               text="FIRST IMAGE (fixed)",
                                                               background_color=Color.CLEAR_BACKGROUND,
                                                               font=Font.BOLD,
                                                               position=(20, 60))
        self.__load_first_image_file_button = Base.create_button(parent_view=self.__root_window,
                                                                 text="Read DICOM file",
                                                                 position=(130, 90),
                                                                 command=lambda: self.read_dicom_file(
                                                                     self.__load_first_image_file_button))
        self.__load_first_image_folder_button = Base.create_button(parent_view=self.__root_window,
                                                                   text="Read DICOM folder",
                                                                   position=(250, 90),
                                                                   command=lambda: self.read_dicom_folder(
                                                                       self.__load_first_image_folder_button))

        self.__second_image_title_label = Base.create_text_view(self.__root_window,
                                                                text="SECOND IMAGE (moving)",
                                                                background_color=Color.CLEAR_BACKGROUND,
                                                                font=Font.BOLD,
                                                                position=(20, 140))
        self.__load_second_image_file_button = Base.create_button(parent_view=self.__root_window,
                                                                  text="Read DICOM file",
                                                                  position=(130, 170),
                                                                  command=lambda: self.read_dicom_file(
                                                                      self.__load_second_image_file_button))
        self.__load_second_image_folder_button = Base.create_button(parent_view=self.__root_window,
                                                                    text="Read DICOM folder",
                                                                    position=(250, 170),
                                                                    command=lambda: self.read_dicom_folder(
                                                                        self.__load_second_image_folder_button))

        self.__read_images_button = Base.create_button(parent_view=self.__root_window,
                                                       text="START READING",
                                                       position=(190, 220),
                                                       command=self.start_reading_files)

    def read_dicom_file(self, button):
        """
        Reads the DICOM file.

        Args:
            button: The selected button.
        """
        file_path = filedialog.askopenfilename(initialdir="/",
                                               title="Select a file",
                                               filetypes=(("DICOM files", "*.dcm"), ("All files", "*.*")))

        if file_path != "" or file_path is not None:
            if button is self.__load_first_image_file_button:
                self.__first_image_file = SelectedFile(True, file_path)
            elif button is self.__load_second_image_file_button:
                self.__second_image_file = SelectedFile(True, file_path)

    def read_dicom_folder(self, button):
        """
        Reads the DICOM folder.

        Args:
            button: The selected button.
        """
        folder_path = filedialog.askdirectory(initialdir="/",
                                              title="Select a directory")

        if folder_path != "" or folder_path is not None:
            if button is self.__load_first_image_folder_button:
                self.__first_image_file = SelectedFile(False, folder_path)
            elif button is self.__load_second_image_folder_button:
                self.__second_image_file = SelectedFile(False, folder_path)

    def start_reading_files(self):
        """
        Closes the window and notifies the controller that the image selection has finished.
        """
        if self.__first_image_file is None or self.__second_image_file is None:
            messagebox.showerror("Error while reading", "Some image has not been selected. Please, try again.")
        else:
            self.__listener(RegisteringListenerCode.SELECTED_IMAGES,
                            first_image=self.__first_image_file,
                            second_image=self.__second_image_file)
            self.__root_window.destroy()
            self.__root_window.update()
