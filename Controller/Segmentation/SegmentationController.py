from Controller.Segmentation.SegmentationListenerCode import SegmentationListenerCode
from Model.Segmentation.SegmentationModel import SegmentationModel
from View.Segmentation import SegmentationGUI


class SegmentationController:

    def __init__(self):
        """
        Initializes the object that manages the events in the execution.
        """
        self.__model = SegmentationModel(self.controller_listener)

        self.__root_view, self.__view = SegmentationGUI.show_main_view(self.controller_listener)
        self.__root_view.mainloop()

    def controller_listener(self, action_code: SegmentationListenerCode, **kwargs):
        """
        Listener of the different events that occur in the GUI or in the model.

        Args:
            action_code: A ListenerCode value, representing the action to handle.
            **kwargs: Arguments of the action.
        """
        if action_code == SegmentationListenerCode.DID_PICKED_IMAGE:
            file = kwargs['file']
            self.__model.load_dicom_image(file)
        elif action_code == SegmentationListenerCode.DID_LOAD_IMAGE:
            read_image = kwargs['image']
            z_axis_limit = kwargs['z_axis_limit']
            tensor_range = kwargs['tensor_range']

            self.__view.enable_widgets()
            self.__view.set_slider_limit(0, z_axis_limit)
            self.__view.set_segmentation_methods_slider_limit(lower_limit=tensor_range[0], upper_limit=tensor_range[1])
            self.__view.set_images(original_image=read_image)
        elif action_code == SegmentationListenerCode.VISUALIZATION_PARAMETERS_DID_CHANGE:
            slice_image = self.__model.get_slice_image(kwargs['axis'], kwargs['slice'])
            segmented_mask, segmented_marked = self.__model.segment_image(slice_image, kwargs['segmentation_settings'])

            self.__view.set_images(original_image=slice_image,
                                   mask_image=segmented_mask,
                                   marked_image=segmented_marked)

        elif action_code == SegmentationListenerCode.AXIS_DID_CHANGE:
            self.__view.set_slider_limit(0, self.__model.get_range(kwargs['axis']))
