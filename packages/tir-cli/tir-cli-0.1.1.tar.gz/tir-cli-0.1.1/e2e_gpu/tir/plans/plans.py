from e2enetworks.cloud.tir import Plans
from e2enetworks.constants import INFERENCE, NOTEBOOK

from e2e_gpu.core.cli_helpers import get_output
from e2e_gpu.core.constants import (CONFIRMATION_MSG, CREATE, DEFAULT, DELETE,
                                    GET, HELP, LIST, UPDATE, USER_INTERRUPTS,
                                    YES)
from e2e_gpu.tir.plans.plan_parser import parse_for_listing


class PlansService:

    def __init__(self, parser, plans_inputs_parser):
        self.parser = parser
        self.plans_inputs_parser = plans_inputs_parser
        self.arguments = None

    def __call__(self, plans_command):
        operations_set = {LIST: self.list_plans, }
        operation = operations_set.get(plans_command)
        if operation:
            operation()

    def list_plans(self):
        parse_for_listing(self)
        response = {}
        if self.arguments.service == NOTEBOOK:
            Plans().get_notebook_plans_name(image=self.arguments.image_id)
        elif self.arguments.service == INFERENCE:
            Plans().list_endpoint_plans()
