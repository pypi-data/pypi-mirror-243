from e2e_gpu.core.cli_helpers import exit_process
from e2e_gpu.core.config_service import get_user_cred
from e2e_gpu.core.constants import (CONFIRMATION_MSG, CREATE, DEFAULT, DELETE,
                                    GET, HELP, LIST, UPDATE, USER_INTERRUPTS,
                                    YES)
from e2e_gpu.tir.images.image_parser import parse_images_command
from e2e_gpu.tir.images.images import ImagesService


class ImagesRouting:
    def __init__(self, parser, images_parser):
        self.parser = parser
        self.images_parser = images_parser
        self.service_parser_mapping = parse_images_command(images_parser)
        self.arguments = parser.parse_known_args()[0]
        self.images_inputs_parser = self.service_parser_mapping.get(self.arguments.images_command)

    def __call__(self):
        if self.arguments.images_command != HELP and self.images_inputs_parser:
            service = ImagesService(self.parser, self.images_inputs_parser)
            service(self.arguments.images_command)
        else:
            self.images_parser.print_help()
            exit_process()
