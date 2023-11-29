from e2enetworks.constants import BUCKET_TYPES, MANAGED_STORAGE

from e2e_gpu.core.cli_helpers import exit_process
from e2e_gpu.core.constants import CREATE, DELETE, GET, HELP, LIST, UPDATE
from e2e_gpu.tir.datasets.constants import DOWNLOAD_DATASET, PUSH_DATASET
from e2e_gpu.tir.datasets.validators import (_creation_is_valid,
                                             _delete_get_request_is_valid,
                                             _download_is_valid,
                                             _upload_is_valid)


def parse_dataset_command(dataset_parser):
    dataset_sub_parser = dataset_parser.add_subparsers(
        title="Dataset Commands", metavar="", dest="dataset_commands")
    dataset_parser.usage = "tir [--project] dataset [dataset_command] ..."

    dataset_create_parser = dataset_sub_parser.add_parser(
        CREATE, help="Creates a new dataset with the provided name, bucket name, bucket_type and description", add_help=False)
    dataset_delete_parser = dataset_sub_parser.add_parser(
        DELETE, help="Deletes a dataset with the given bucket name.", add_help=False)
    dataset_list_parser = dataset_sub_parser.add_parser(
        LIST, help="Lists all datasets associated with the team and project.", add_help=False)
    dataset_get_parser = dataset_sub_parser.add_parser(
        GET, help="Retrieves information about a specific dataset using its bucket name.", add_help=False)
    dataset_push_dataset_parser = dataset_sub_parser.add_parser(
        PUSH_DATASET, help="Used to push a dataset to the a specific dataset_storage using its dataset_id", add_help=False)
    dataset_download_dataset_parser = dataset_sub_parser.add_parser(
        DOWNLOAD_DATASET, help="Used to download dataset from a specific dataset_storage using its dataset_id", add_help=False)
    dataset_help_parser = dataset_sub_parser.add_parser(
        HELP, help="To display help msg and exit")

    parser_mapping = {CREATE: dataset_create_parser,
                      LIST: dataset_list_parser,
                      GET: dataset_get_parser,
                      DELETE: dataset_delete_parser,
                      PUSH_DATASET: dataset_push_dataset_parser,
                      DOWNLOAD_DATASET: dataset_download_dataset_parser}

    return parser_mapping


def parse_for_creation(obj):
    datset_inputs_parser = obj.datset_inputs_parser
    datset_inputs_parser.usage = "tir [--project] dataset create ..."

    dataset_create_name = datset_inputs_parser.add_argument("--name", required=False, metavar="",
                                                            help="Creates a new dataset with the provided name, bucket_name, bucket_type and description")
    dataset_create_bucket_type = datset_inputs_parser.add_argument("--bucket_type", default=MANAGED_STORAGE, choices=BUCKET_TYPES, metavar="",
                                                                   help="Lists all datasets associated with the team and project.")
    dataset_create_bucket_name = datset_inputs_parser.add_argument("--bucket_name", required=False, metavar="",
                                                                   help="Deletes a dataset with the given bucket name.")
    dataset_create_description = datset_inputs_parser.add_argument("--description", required=False, metavar="",
                                                                   help="Retrieves information about a specific dataset using its bucket name.")
    _help = datset_inputs_parser.add_argument(HELP, action='store_true', default=False,
                                                            help="To display help msg and exit")

    obj.arguments = obj.parser.parse_known_args()[0]
    if obj.arguments.help or not _creation_is_valid(obj.arguments):
        obj.datset_inputs_parser.print_help()
        exit_process()


def parse_for_deletion(obj):
    datset_inputs_parser = obj.datset_inputs_parser
    datset_inputs_parser.usage = "tir [--project] dataset delete ..."

    dataset_id = datset_inputs_parser.add_argument("--dataset_id", required=False, type=int, metavar="",
                                                   help="id of dataset to be deleted")
    _help = datset_inputs_parser.add_argument(HELP, action='store_true', default=False,
                                                         help="To display help msg and exit")

    obj.arguments = obj.parser.parse_known_args()[0]
    if obj.arguments.help or not _delete_get_request_is_valid(obj.arguments):
        obj.datset_inputs_parser.print_help()
        exit_process()


def parse_for_get_info(obj):
    datset_inputs_parser = obj.datset_inputs_parser
    datset_inputs_parser.usage = "tir [--project] dataset get ..."

    dataset_id = datset_inputs_parser.add_argument("--dataset_id", required=False, type=int, metavar="",
                                                   help="id of dataset to be deleted")
    _help = datset_inputs_parser.add_argument(HELP, action='store_true', default=False,
                                                         help="To display help msg and exit")

    obj.arguments = obj.parser.parse_known_args()[0]
    if obj.arguments.help or not _delete_get_request_is_valid(obj.arguments):
        obj.datset_inputs_parser.print_help()
        exit_process()


def parse_for_dataset_download(obj):
    
    dataset_inputs_parser = obj.dataset_inputs_parser
    dataset_inputs_parser.usage = "tir [--project] dataset download ..."

    dataset_id = dataset_inputs_parser.add_argument("--dataset_id", required=False, type=int, metavar="",
                                                    help="id of dataset to be downloaded")
    local_path = dataset_inputs_parser.add_argument("--local_path", required=False, metavar="",
                                                    help="local path, where dataset is to be downloaded")
    prefix = dataset_inputs_parser.add_argument("--prefix", default="", metavar="",
                                                help="Type of dataset you want to create")
    dataset_help = dataset_inputs_parser.add_argument(HELP, action='store_true', default=False,
                                                             help="To display help msg and exit")
    
    obj.arguments = obj.parser.parse_known_args()[0]
    if obj.arguments.help or not _download_is_valid(obj.arguments):
        obj.dataset_inputs_parser.print_help()
        exit_process()


def parse_for_dataset_upload(obj):
    dataset_inputs_parser = obj.dataset_inputs_parser
    dataset_inputs_parser.usage = "tir [--project] dataset push ..."

    dataset_id = dataset_inputs_parser.add_argument("--dataset_id", required=False, type=int, metavar="",
                                                    help="id of dataset to be uploaded")
    dataset_path = dataset_inputs_parser.add_argument("--dataset_path", required=False, metavar="",
                                                      help="path from where dataset is to be uploaded")
    prefix = dataset_inputs_parser.add_argument("--prefix", default="", metavar="",
                                                help="Type of dataset you want to create")
    dataset_create_help = dataset_inputs_parser.add_argument(HELP, action='store_true', default=False,
                                                             help="To display help msg and exit")

    obj.arguments = obj.parser.parse_known_args()[0]
    if obj.arguments.help or not _upload_is_valid(obj.arguments):
        obj.dataset_inputs_parser.print_help()
        exit_process()
