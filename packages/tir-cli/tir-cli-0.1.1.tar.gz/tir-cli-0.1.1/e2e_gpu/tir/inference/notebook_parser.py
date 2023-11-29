from e2e_gpu.core.cli_helpers import exit_process
from e2e_gpu.core.constants import CREATE, DELETE, GET, HELP, LIST
from e2e_gpu.tir.notebooks.constants import START, STOP, UPGRADE
from e2e_gpu.tir.notebooks.validators import (_creation_is_valid,
                                              _notebook_id_exists,
                                              _upgrade_request_is_valid)


def parse_notebook_command(notebook_parser):

    config_sub_parser = notebook_parser.add_subparsers(
        title="notebook Commands", metavar="", dest="notebook_command")
    notebook_parser.usage = "tir [--project] notebook [notebook_command] ..."

    notebook_create_parser = config_sub_parser.add_parser(
        CREATE, help="Creates a new notebook with the provided name, bucket_name, notebook_type and storage_type", add_help=False)
    notebook_delete_parser = config_sub_parser.add_parser(
        DELETE, help="Deletes a notebook with the given notebook_id", add_help=False)
    notebook_list_parser = config_sub_parser.add_parser(
        LIST, help="Lists all notebooks associated with the team and project.", add_help=False)
    notebook_get_parser = config_sub_parser.add_parser(
        GET, help="Retrieves information about a specific notebook using its notebook_id", add_help=False)
    notebook_start_parser = config_sub_parser.add_parser(
        START, help="used to start a notebook, using its notebook_id", add_help=False)
    notebook_stop_parser = config_sub_parser.add_parser(
        STOP, help="used to stop a notebook, using its notebook_id", add_help=False)
    notebook_upgrade_parser = config_sub_parser.add_parser(
        UPGRADE, help="used to upgrade a notebook disk size, using its notebook_id", add_help=False)
    notebook_help_parser = config_sub_parser.add_parser(
        HELP, help="To display help msg and exit")

    parser_mapping = {CREATE: notebook_create_parser,
                      LIST: notebook_list_parser,
                      GET: notebook_get_parser,
                      DELETE: notebook_delete_parser,
                      START: notebook_start_parser,
                      STOP: notebook_stop_parser,
                      UPGRADE: notebook_upgrade_parser}

    return parser_mapping


def parse_for_creation(obj):
    notebook_inputs_parser = obj.notebook_inputs_parser
    notebook_inputs_parser.usage = "tir [--project] notebook create ..."

    notebook_name = notebook_inputs_parser.add_argument("--name", required=False, metavar="",
                                                         help="Name of the a new notebook")
    notebook_plan = notebook_inputs_parser.add_argument("--plan_name", required=False, metavar="",
                                                               help="Type of notebook you want to create")
    notebook_image_id = notebook_inputs_parser.add_argument("--image_id", type=int, metavar="",
                                                                 help="Lists all notebooks associated with the team and project.")
    disk_size = notebook_inputs_parser.add_argument("--disk_size", type =int, default=30, metavar="",
                                                                help="Name of bucket, you want to store your notebook in")
    notebook_type = notebook_inputs_parser.add_argument("--notebook_type", default="new", metavar="",
                                                                help="Name of bucket, you want to store your notebook in")
    notebook_url = notebook_inputs_parser.add_argument("--notebook_url", default="", metavar="",
                                                                help="Name of bucket, you want to store your notebook in")
    notebook_create_help = notebook_inputs_parser.add_argument(HELP, action='store_true', default=False,
                                                         help="To display help msg and exit")

    obj.arguments = obj.parser.parse_known_args()[0]
    if obj.arguments.help or not _creation_is_valid(obj.arguments):
        obj.notebook_inputs_parser.print_help()
        exit_process()


def parse_for_delete_get_start_stop_request(obj):
    notebook_inputs_parser = obj.notebook_inputs_parser
    notebook_inputs_parser.usage = "tir [--project] notebook delete ..."

    notebook_id = notebook_inputs_parser.add_argument("--notebook_id", required=False, type=int, metavar="",
                                                help="id of notebook to be deleted")
    _help = notebook_inputs_parser.add_argument(HELP, action='store_true', default=False,
                                                         help="To display help msg and exit")

    obj.arguments = obj.parser.parse_known_args()[0]
    if obj.arguments.help or not _notebook_id_exists(obj.arguments):
        obj.notebook_inputs_parser.print_help()
        exit_process()


def parse_for_upgrade(obj):
    notebook_inputs_parser = obj.notebook_inputs_parser
    notebook_inputs_parser.usage = "tir [--project] notebook get ..."

    notebook_id = notebook_inputs_parser.add_argument("--notebook_id", required=False, type=int, metavar="",
                                                help="id of notebook to be fetch")
    disk_size = notebook_inputs_parser.add_argument("--disk_size", required=False, type=int, metavar="",
                                                help="id of notebook to be fetch")
    notebook_get_help = notebook_inputs_parser.add_argument(HELP, action='store_true', default=False,
                                                         help="To display help msg and exit")

    obj.arguments = obj.parser.parse_known_args()[0]
    if obj.arguments.help or not _upgrade_request_is_valid(obj.arguments):
        obj.notebook_inputs_parser.print_help()
        exit_process()
