from e2e_gpu.core.cli_helpers import exit_process
from e2e_gpu.core.config_service import get_user_cred
from e2e_gpu.core.constants import (CONFIRMATION_MSG, CREATE, DEFAULT, DELETE,
                                    GET, HELP, LIST, UPDATE, USER_INTERRUPTS,
                                    YES)
from e2e_gpu.tir.models.model_parser import parse_model_command
from e2e_gpu.tir.models.models import ModelService


class ModelRouting:
    def __init__(self, parser, model_parser):
        self.parser = parser
        self.model_parser = model_parser
        self.service_parser_mapping = parse_model_command(model_parser)
        self.arguments = parser.parse_known_args()[0]
        self.model_inputs_parser = self.service_parser_mapping.get(self.arguments.model_command)

    def __call__(self):
        if self.arguments.model_command != HELP and self.model_inputs_parser:
            service = ModelService(self.parser, self.model_inputs_parser)
            service(self.arguments.model_command)
        else:
            self.model_parser.print_help()
            exit_process()
