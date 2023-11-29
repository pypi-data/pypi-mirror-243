from e2e_gpu.commands_routing import CommandsRouting
from e2e_gpu.core.constants import (CONFIG, DATASETS, DEFAULT, ENDPOINTS,
                                    IMAGES, MODELS, NOTEBOOK, PIPELINES, PLANS,
                                    PROJECTS, SKUS, TEAMS)
from e2e_gpu.e2e_parser import ArgumentParser as ArgParser
from e2e_gpu.e2e_parser import RawTextHelpFormatter


def commanding(parser):
    sub_parser = parser.add_subparsers(
        title="Commands", metavar="", dest="command")
    parser.usage = "tir [--version] [--info] [--debug] [--project] Command  ..."

    config_parser = sub_parser.add_parser(
        CONFIG, help="To add/remove tokens", add_help=False, formatter_class=RawTextHelpFormatter)
    datasets_parser = sub_parser.add_parser(
        DATASETS, help="To create/delete/list datasets of the user", add_help=False, formatter_class=RawTextHelpFormatter)
    endpoints_parser = sub_parser.add_parser(
        ENDPOINTS, help="To apply operations over endpoints", add_help=False, formatter_class=RawTextHelpFormatter)
    image_parser = sub_parser.add_parser(
        IMAGES, help="To list available Image", add_help=False, formatter_class=RawTextHelpFormatter)
    models_parser = sub_parser.add_parser(
        MODELS, help="To perform operations over models", add_help=False, formatter_class=RawTextHelpFormatter)
    notebook_parser = sub_parser.add_parser(
        NOTEBOOK, help="To apply crud operations over notebook", add_help=False, formatter_class=RawTextHelpFormatter)
    pipelines_parser = sub_parser.add_parser(
        PIPELINES, help="To create/delete/list pipelines ", add_help=False, formatter_class=RawTextHelpFormatter)
    plans_parser = sub_parser.add_parser(
        PLANS, help="To list available plans", add_help=False, formatter_class=RawTextHelpFormatter)
    projects_parser = sub_parser.add_parser(
        PROJECTS, help="To perform operations over projects", add_help=False, formatter_class=RawTextHelpFormatter)
    skus_parser = sub_parser.add_parser(
        SKUS, help="To list SKUS", add_help=False, formatter_class=RawTextHelpFormatter)
    teams_parser = sub_parser.add_parser(
        TEAMS, help="To create/delete/list teams for the user", add_help=False, formatter_class=RawTextHelpFormatter)

    parser.add_argument("--help", action='store_true', default=False,
                        help="To display help msg and exit")

    command_parser_mapping = {CONFIG: config_parser, DATASETS: datasets_parser,
                              ENDPOINTS: endpoints_parser, IMAGES: image_parser,
                              MODELS: models_parser, NOTEBOOK: notebook_parser,
                              PIPELINES: pipelines_parser, PLANS: plans_parser, 
                              PROJECTS: projects_parser, SKUS: skus_parser, 
                              TEAMS: teams_parser}
    command_parser = command_parser_mapping.get(parser.parse_known_args()[0].command)
    return command_parser


def run_main_class():
    parser = ArgParser(description="TIR CLI", add_help=False,
                       formatter_class=RawTextHelpFormatter)

    # version, pkg-info, alias, project to be taken first else default
    parser.add_argument("-v", "--version", action='store_true',
                        help="To view version info")
    parser.add_argument("--info", action='store_true',
                        help="To view package info")
    parser.add_argument("--debug", action='store_true',
                        help="To view detailed error info")
    parser.add_argument("--project", default=DEFAULT, type=str,
                        help="The name of your tir-project, as saved on your system")

    command_sub_parser = commanding(parser)
    route = CommandsRouting(parser, command_sub_parser)
    route()
