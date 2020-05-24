import tkinter as tk

from Controller.Segmentation.SegmentationListenerCode import SegmentationListenerCode
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

        self.__image_file: SelectedFile = None

        self.__title_label = Base.create_text_view(self.__root_window,
                                                   text="Select a DICOM file. Only DICOM files or folders are allowed.",
                                                   background_color=Color.CLEAR_BACKGROUND,
                                                   font=Font.REGULAR,
                                                   position=(20, 20))

        self.__load_dicom_file = Base.create_button(parent_view=self.__root_window,
                                                    text="Read DICOM file",
                                                    position=(130, 90),
                                                    command=self.read_dicom_file)
        self.__load_dicom_folder = Base.create_button(parent_view=self.__root_window,
                                                      text="Read DICOM folder",
                                                      position=(250, 90),
                                                      command=self.read_dicom_folder)

        self.__read_images_button = Base.create_button(parent_view=self.__root_window,
                                                       text="START READING",
                                                       position=(190, 150),
                                                       command=self.start_reading_files)

    def read_dicom_file(self):
        """
        Reads the DICOM file.
        """
        file_path = filedialog.askopenfilename(initialdir="/",
                                               title="Select a file",
                                               filetypes=(("DICOM files", "*.dcm"), ("All files", "*.*")))

        if file_path != "" or file_path is not None:
            self.__image_file = SelectedFile(True, file_path)

    def read_dicom_folder(self):
        """
        Reads the DICOM folder.
        """
        folder_path = filedialog.askdirectory(initialdir="/",
                                              title="Select a directory")

        if folder_path != "" or folder_path is not None:
            self.__image_file = SelectedFile(False, folder_path)

    def start_reading_files(self):
        """
        Closes the window and notifies the controller that the image selection has finished.
        """
        if self.__image_file is None:
            messagebox.showerror("Error while reading", "Any image has not been selected. Please, try again.")
        else:
            self.__listener(SegmentationListenerCode.DID_PICKED_IMAGE,
                            file=self.__image_file)
            self.__root_window.destroy()
            self.__root_window.update()
