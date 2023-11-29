from e2enetworks.cloud.tir.images import Images

from e2e_gpu.core.cli_helpers import get_output
from e2e_gpu.core.constants import (CONFIRMATION_MSG, CREATE, DEFAULT, DELETE,
                                    GET, HELP, LIST, UPDATE, USER_INTERRUPTS,
                                    YES)


class ImagesService:

    def __init__(self, parser, images_inputs_parser):
        self.parser = parser
        self.images_inputs_parser = images_inputs_parser
        self.arguments = None

    def __call__(self, images_command):
        operations_set = {LIST: self.list_images, }
        operation = operations_set.get(images_command)
        if operation:
            operation()

    def list_images(self):
        response = Images().list()
        print(response)

    