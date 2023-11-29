from e2e_gpu.core.cli_helpers import exit_process
from e2e_gpu.core.config_service import get_user_cred
from e2e_gpu.core.constants import (CONFIRMATION_MSG, CREATE, DEFAULT, DELETE,
                                    GET, HELP, LIST, UPDATE, USER_INTERRUPTS,
                                    YES)
from e2e_gpu.tir.plans.plan_parser import parse_plans_command
from e2e_gpu.tir.plans.plans import PlansService


class PlansRouting:
    def __init__(self, parser, plans_parser):
        self.parser = parser
        self.plans_parser = plans_parser
        self.service_parser_mapping = parse_plans_command(plans_parser)
        self.arguments = parser.parse_known_args()[0]
        self.plans_inputs_parser = self.service_parser_mapping.get(self.arguments.plans_command)

    def __call__(self):
        if self.arguments.plans_command != HELP and self.plans_inputs_parser:
            service = PlansService(self.parser, self.plans_inputs_parser)
            service(self.arguments.plans_command)
        else:
            self.plans_parser.print_help()
            exit_process()
