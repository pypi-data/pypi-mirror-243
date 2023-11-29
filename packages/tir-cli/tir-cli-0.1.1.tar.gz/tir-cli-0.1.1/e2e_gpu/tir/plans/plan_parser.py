from e2enetworks.constants import INFERENCE, NOTEBOOK

from e2e_gpu.core.cli_helpers import exit_process
from e2e_gpu.core.constants import CREATE, DELETE, GET, HELP, LIST, UPDATE



def parse_plans_command(plans_parser):
    plan_sub_parser = plans_parser.add_subparsers(
        title="plans Commands", metavar="", dest="plans_command")
    plans_parser.usage = "tir [--project] plans [plans_command] ..."

    plans_list_parser = plan_sub_parser.add_parser(
        LIST, help="Lists all plans available", add_help=False)
    help_parser = plan_sub_parser.add_parser(
        HELP, help="To display help msg and exit")

    parser_mapping = {LIST: plans_list_parser,}

    return parser_mapping

def parse_for_listing(obj):
    plans_inputs_parser = obj.plans_inputs_parser
    plans_inputs_parser.usage = "tir [--project] plans delete ..."

    service = plans_inputs_parser.add_argument("--service", required=False, choices=[INFERENCE, NOTEBOOK], metavar="",
                                                help="Name of service for which are to be listed")
    image_id = plans_inputs_parser.add_argument("--image_id", required=False, type=int, metavar="",
                                                help="Name of service for which are to be listed")
    plans_delete_help = plans_inputs_parser.add_argument(HELP, action='store_true', default=False,
                                                         help="To display help msg and exit")

    obj.arguments = obj.parser.parse_known_args()[0]
    if obj.arguments.help or not obj.arguments.service:
        obj.plans_inputs_parser.print_help()
        exit_process()
