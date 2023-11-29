from e2e_gpu.core.cli_helpers import exit_process
from e2e_gpu.core.config_service import get_user_cred
from e2e_gpu.core.constants import (CONFIRMATION_MSG, CREATE, DEFAULT, DELETE,
                                    GET, HELP, LIST, UPDATE, USER_INTERRUPTS,
                                    YES)
from e2e_gpu.tir.notebooks.notebook_parser import parse_notebook_command
from e2e_gpu.tir.notebooks.notebooks import NotebookService


class NotebookRouting:
    def __init__(self, parser, notebook_parser):
        self.parser = parser
        self.notebook_parser = notebook_parser
        self.service_parser_mapping = parse_notebook_command(notebook_parser)
        self.arguments = parser.parse_known_args()[0]
        self.notebook_inputs_parser = self.service_parser_mapping.get(self.arguments.notebook_command)

    def __call__(self):
        if self.arguments.notebook_command != HELP and self.notebook_inputs_parser:
            service = NotebookService(self.parser, self.notebook_inputs_parser)
            service(self.arguments.notebook_command)
        else:
            self.notebook_parser.print_help()
            exit_process()
