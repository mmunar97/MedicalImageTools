from Controller.Registering.RegisteringListenerCode import RegisteringListenerCode
from Model.Registering.RegisteringModel import RegisteringModel
from View.Registering import RegisterGUI


class RegisteringController:

    def __init__(self):
        """
        Initializes the object that manages the events in the execution.
        """
        self.__model = RegisteringModel(self.controller_listener)

        self.__root_view, self.__view = RegisterGUI.show_main_view(self.controller_listener)
        self.__root_view.mainloop()

    def controller_listener(self, action_code: RegisteringListenerCode, **kwargs):
        """
        Listener of the different events that occur in the GUI or in the model.

        Args:
            action_code: A ListenerCode value, representing the action to handle.
            **kwargs: Arguments of the action.
        """
        if action_code == RegisteringListenerCode.SELECTED_IMAGES:
            first_image_file = kwargs['first_image']
            second_image_file = kwargs['second_image']

            self.__model.set_picked_files(first_image_file, second_image_file)

        elif action_code == RegisteringListenerCode.IMAGES_READ:
            self.__view.show_read_status(kwargs['status'])
            if kwargs['status'] == 1:
                self.__view.enable_widgets()
                self.__view.set_slider_limit(0, kwargs['upper_limit'])

                image1, image2, alpha_image, registered = self.__model.get_tensor_images(axis=0,
                                                                                         slice=0,
                                                                                         alpha=100)
                self.__view.set_images(image1, image2, alpha_image, registered)

        elif action_code == RegisteringListenerCode.RADIO_BUTTON_CHANGED:
            limit = self.__model.get_tensor_limit_for_axis(axis=kwargs['axis'])
            self.__view.set_slider_limit(0, limit)

            image1, image2, alpha_image, registered = self.__model.get_tensor_images(axis=kwargs['axis'],
                                                                                     slice=0,
                                                                                     alpha=100)
            self.__view.set_images(image1, image2, alpha_image, registered)

        elif action_code == RegisteringListenerCode.SLICE_SLIDER_CHANGED or \
                action_code == RegisteringListenerCode.ALPHA_SLIDER_CHANGED:
            image1, image2, alpha_image, registered = self.__model.get_tensor_images(axis=kwargs['axis'],
                                                                                     slice=kwargs['slice'],
                                                                                     alpha=kwargs['alpha'])
            self.__view.set_images(image1, image2, alpha_image, registered)

        elif action_code == RegisteringListenerCode.REGISTERING_WILL_START:
            self.__model.register_images(**kwargs)

        elif action_code == RegisteringListenerCode.REGISTERING_DID_FINISH:
            self.__view.end_registration()
