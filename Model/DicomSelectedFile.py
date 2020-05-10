from os import listdir

import numpy
import pydicom


class DicomSelectedFile():

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
            self.read_file()
        else:
            self.read_folder()

    def read_file(self):
        """
        Reads the selected file.
        """
        self.dicom_file = pydicom.read_file(self.__path)
        self.image_tensor = self.dicom_file.pixel_array

        print(self.image_tensor.shape)

    def read_folder(self):
        """
        Reads all the DICOM files in the folder.
        """
        files_list = sorted(listdir(self.__path))

        self.dicom_file = pydicom.read_file(self.__path + '/' + files_list[0])
        tensor = numpy.zeros((self.dicom_file.pixel_array.shape[0],
                              self.dicom_file.pixel_array.shape[1],
                              len(files_list)))

        for file_index, file in enumerate(sorted(listdir(self.__path))):
            if ".dcm" in file:
                temp_dicom_file = pydicom.read_file(self.__path+'/'+file)
                tensor[:, :, file_index] = temp_dicom_file.pixel_array

        self.image_tensor = tensor
