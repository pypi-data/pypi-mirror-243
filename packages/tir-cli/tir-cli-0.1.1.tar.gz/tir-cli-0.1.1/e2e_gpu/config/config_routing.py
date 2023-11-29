from e2e_gpu.config.config import AuthConfig
from e2e_gpu.core.cli_helpers import exit_process
from e2e_gpu.core.config_service import get_user_cred
from e2e_gpu.core.constants import (CONFIRMATION_MSG, DEFAULT, USER_INTERRUPTS,
                                    YES)


class ConfigRouting:
    def __init__(self, parser, config_parser):
        self.parser = parser
        self.config_parser = config_parser
        self.arguments = parser.parse_known_args()[0]

    def route(self):

        if self.arguments.config_commands == 'add':
            try:
                auth_config_object = AuthConfig(alias=input("Input name of project you want to add : "))
                auth_config_object.add_to_config()
            except USER_INTERRUPTS:
                exit_process()

        elif self.arguments.config_commands == 'remove':
            delete_project = input("Input name of project you want to delete : ")
            confirmation = input(CONFIRMATION_MSG)
            if (confirmation.lower() == YES):
                auth_config_object = AuthConfig(project=delete_project)
                try:
                    auth_config_object.delete_from_config()
                except USER_INTERRUPTS:
                    exit_process()

        elif self.arguments.config_commands == 'list':
            try:
                print("Saved Projects :")
                for item in list(get_user_cred("all", 1)):
                    print(item)
            except USER_INTERRUPTS:
                exit_process()

        elif self.arguments.config_commands == 'set':
            default_name = input("Enter name of the project you want to set as default : ")
            if (input(CONFIRMATION_MSG).lower() == YES):
                try:
                    AuthConfig(project=DEFAULT).delete_from_config(x=1)
                    auth_config_object = AuthConfig(project=default_name)
                    auth_config_object.set_default()
                    print("Default alias set to ", default_name)
                except USER_INTERRUPTS:
                    exit_process()

        else:
            self.config_parser.print_help()
