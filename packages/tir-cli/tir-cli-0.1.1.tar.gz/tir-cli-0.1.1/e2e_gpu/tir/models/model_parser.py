from e2enetworks.constants import MANAGED_STORAGE, MODEL_TYPES

from e2e_gpu.core.cli_helpers import exit_process
from e2e_gpu.core.constants import CREATE, DELETE, GET, HELP, LIST, UPDATE
from e2e_gpu.tir.models.constants import DOWNLOAD_MODEL, PUSH_MODEL
from e2e_gpu.tir.models.validators import (_creation_is_valid,
                                           _delete_get_request_is_valid,
                                           _download_is_valid,
                                           _upload_is_valid)


def parse_model_command(model_parser):

    config_sub_parser = model_parser.add_subparsers(
        title="model Commands", metavar="", dest="model_command")
    model_parser.usage = "tir [--project] model [model_command] ..."

    model_create_parser = config_sub_parser.add_parser(
        CREATE, help="Creates a new model with the provided name, bucket_name, model_type and storage_type", add_help=False)
    model_delete_parser = config_sub_parser.add_parser(
        DELETE, help="Deletes a model with the given model_id", add_help=False)
    model_list_parser = config_sub_parser.add_parser(
        LIST, help="Lists all models associated with the team and project.", add_help=False)
    model_get_parser = config_sub_parser.add_parser(
        GET, help="Retrieves information about a specific model using its model_id", add_help=False)
    model_push_model_parser = config_sub_parser.add_parser(
        PUSH_MODEL, help="Used to push a model to the a specific model_storage using its model_id", add_help=False)
    model_download_model_parser = config_sub_parser.add_parser(
        DOWNLOAD_MODEL, help="Used to download model from a specific model_storage using its model_id", add_help=False)
    model_help_parser = config_sub_parser.add_parser(
        HELP, help="To display help msg and exit")

    parser_mapping = {CREATE: model_create_parser,
                      LIST: model_list_parser,
                      GET: model_get_parser,
                      DELETE: model_delete_parser,
                      PUSH_MODEL: model_push_model_parser,
                      DOWNLOAD_MODEL: model_download_model_parser}

    return parser_mapping


def parse_for_creation(obj):
    model_inputs_parser = obj.model_inputs_parser
    model_inputs_parser.usage = "tir [--project] model create ..."

    model_create_name = model_inputs_parser.add_argument("--name", required=False, metavar="",
                                                         help="Name of the a new model")
    model_create_model_type = model_inputs_parser.add_argument("--model_type", required=False, choices=MODEL_TYPES, metavar="",
                                                               help="Type of model you want to create")
    model_create_storage_type = model_inputs_parser.add_argument("--storage_type", default=MANAGED_STORAGE, metavar="",
                                                                 help="Lists all models associated with the team and project.")
    model_create_bucket_name = model_inputs_parser.add_argument("--bucket_name", required=False, metavar="",
                                                                help="Name of bucket, you want to store your model in")
    model_create_help = model_inputs_parser.add_argument(HELP, action='store_true', default=False,
                                                         help="To display help msg and exit")

    obj.arguments = obj.parser.parse_known_args()[0]
    if obj.arguments.help or not _creation_is_valid(obj.arguments):
        obj.model_inputs_parser.print_help()
        exit_process()


def parse_for_deletion(obj):
    model_inputs_parser = obj.model_inputs_parser
    model_inputs_parser.usage = "tir [--project] model delete ..."

    model_id = model_inputs_parser.add_argument("--model_id", required=False, type=int, metavar="",
                                                help="id of model to be deleted")
    model_delete_help = model_inputs_parser.add_argument(HELP, action='store_true', default=False,
                                                         help="To display help msg and exit")

    obj.arguments = obj.parser.parse_known_args()[0]
    if obj.arguments.help or not _delete_get_request_is_valid(obj.arguments):
        obj.model_inputs_parser.print_help()
        exit_process()


def parse_for_get_info(obj):
    model_inputs_parser = obj.model_inputs_parser
    model_inputs_parser.usage = "tir [--project] model get ..."

    model_id = model_inputs_parser.add_argument("--model_id", required=False, type=int, metavar="",
                                                help="id of model to be fetch")
    model_get_help = model_inputs_parser.add_argument(HELP, action='store_true', default=False,
                                                         help="To display help msg and exit")

    obj.arguments = obj.parser.parse_known_args()[0]
    if obj.arguments.help or not _delete_get_request_is_valid(obj.arguments):
        obj.model_inputs_parser.print_help()
        exit_process()


def parse_for_model_download(obj):
    model_inputs_parser = obj.model_inputs_parser
    model_inputs_parser.usage = "tir [--project] model download ..."

    model_id = model_inputs_parser.add_argument("--model_id", required=False, type=int, metavar="",
                                                help="id of model to be downloaded")
    model_create_name = model_inputs_parser.add_argument("--local_path", required=False, metavar="",
                                                         help="local path, where model is to be downloaded")
    model_create_model_type = model_inputs_parser.add_argument("--prefix", default="", metavar="",
                                                               help="Type of model you want to create")
    model_create_help = model_inputs_parser.add_argument(HELP, action='store_true', default=False,
                                                         help="To display help msg and exit")

    obj.arguments = obj.parser.parse_known_args()[0]
    if obj.arguments.help or not _download_is_valid(obj.arguments):
        obj.model_inputs_parser.print_help()
        exit_process()


def parse_for_model_upload(obj):
    model_inputs_parser = obj.model_inputs_parser
    model_inputs_parser.usage = "tir [--project] model push ..."

    model_id = model_inputs_parser.add_argument("--model_id", required=False, type=int, metavar="",
                                                help="id of model to be uploaded")
    model_create_name = model_inputs_parser.add_argument("--model_path", required=False, metavar="",
                                                         help="path from where model is to be uploaded")
    model_create_model_type = model_inputs_parser.add_argument("--model_type", default="custom", choices=MODEL_TYPES, metavar="",
                                                               help="Type of model you want to create")
    model_create_model_type = model_inputs_parser.add_argument("--prefix", default="", metavar="",
                                                               help="Type of model you want to create")
    model_create_help = model_inputs_parser.add_argument(HELP, action='store_true', default=False,
                                                         help="To display help msg and exit")

    obj.arguments = obj.parser.parse_known_args()[0]
    if obj.arguments.help or not _upload_is_valid(obj.arguments):
        obj.model_inputs_parser.print_help()
        exit_process()
