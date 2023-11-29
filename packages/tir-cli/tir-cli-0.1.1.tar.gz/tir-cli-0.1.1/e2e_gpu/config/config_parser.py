from e2e_gpu.config.config_routing import ConfigRouting
from e2e_gpu.core.constants import HELP


class ConfigParser:
    def __init__(self, parser, config_parser):
        self.parser = parser
        self.config_parser = config_parser

    def parse(self):
        config_sub_parser = self.config_parser.add_subparsers(
            title="Config Commands", metavar="", dest="config_commands")
        self.config_parser.usage = "tir [--project] config [config_command] ..."

        config_add_sub_parser = config_sub_parser.add_parser(
            "add", help="To add config/access for a project")
        config_remove_sub_parser = config_sub_parser.add_parser(
            "remove", help="To remove config/access for a project")
        config_list_sub_parser = config_sub_parser.add_parser(
            "list", help="To list all config/access names")
        config_set_default_sub_parser = config_sub_parser.add_parser(
            "set", help="To set default config/access for system")
        config_help_sub_parser = config_sub_parser.add_parser(
            HELP, help="To display help msg and exit")

        ConfigRouting(self.parser, self.config_parser).route()
