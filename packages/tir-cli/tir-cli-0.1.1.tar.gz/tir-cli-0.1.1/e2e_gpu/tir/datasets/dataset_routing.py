from e2e_gpu.core.cli_helpers import exit_process
from e2e_gpu.core.config_service import get_user_cred
from e2e_gpu.core.constants import (CONFIRMATION_MSG, CREATE, DEFAULT, DELETE,
                                    GET, HELP, LIST, UPDATE, USER_INTERRUPTS,
                                    YES)
from e2e_gpu.tir.datasets.dataset_parser import parse_dataset_command
from e2e_gpu.tir.datasets.datasets import DatasetService


class DatasetRouting:
    def __init__(self, parser, dataset_parser):
        self.parser = parser
        self.dataset_parser = dataset_parser
        self.service_parser_mapping = parse_dataset_command(dataset_parser)
        self.arguments = parser.parse_known_args()[0]
        self.dataset_inputs_parser = self.service_parser_mapping.get(self.arguments.dataset_commands)

    def __call__(self):
        if self.arguments.dataset_commands != HELP and self.dataset_inputs_parser:
            service = DatasetService(self.parser, self.dataset_inputs_parser)
            service(self.arguments.dataset_commands)
        else:
            self.dataset_parser.print_help()
            exit_process()
