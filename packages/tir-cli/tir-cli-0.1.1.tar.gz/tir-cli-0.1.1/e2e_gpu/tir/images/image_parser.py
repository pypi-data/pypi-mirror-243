from e2e_gpu.core.cli_helpers import exit_process
from e2e_gpu.core.constants import CREATE, DELETE, GET, HELP, LIST, UPDATE


def parse_images_command(images_parser):
    image_sub_parser = images_parser.add_subparsers(
        title="images Commands", metavar="", dest="images_command")
    images_parser.usage = "tir [--project] images [images_command] ..."

    images_list_parser = image_sub_parser.add_parser(
        LIST, help="Lists all images available", add_help=False)
    help_parser = image_sub_parser.add_parser(
        HELP, help="To display help msg and exit")

    parser_mapping = {LIST: images_list_parser,}

    return parser_mapping
