from os import listdir

import numpy
import pydicom


class SelectedFile:

    def __init__(self, is_file: bool, path: str):

        self.__is_file = is_file
        self.__path = path

        self.dicom_file = None
        self.image_tensor = None

    def read(self):
        """
        Reads the DICOM file depending if the path is a file or a folder.
        """
        if self.__is_file:
            self.__read_file()
        else:
            self.__read_folder()

    def __read_file(self):
        """
        Reads the selected file.
        """
        self.dicom_file = pydicom.read_file(self.__path)
        self.image_tensor = self.dicom_file.pixel_array

    def __read_folder(self):
        """
        Reads all the DICOM files in the folder.
        """
        files_list = sorted(listdir(self.__path))
        pydicom_files = [pydicom.read_file(self.__path+'/'+file) for file in files_list]
        pydicom_files.sort(key=lambda x: x[0x0020, 0x1041]._value, reverse=False)

        self.dicom_file = pydicom_files[0]
        tensor = numpy.zeros((self.dicom_file.pixel_array.shape[0],
                              self.dicom_file.pixel_array.shape[1],
                              len(files_list)))

        for file_index, file in enumerate(pydicom_files):
                tensor[:, :, file_index] = file.pixel_array

        self.image_tensor = tensor
