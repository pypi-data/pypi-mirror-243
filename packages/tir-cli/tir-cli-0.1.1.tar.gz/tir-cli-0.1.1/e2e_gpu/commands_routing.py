from e2enetworks.cloud import tir

from e2e_gpu.config.config_parser import ConfigParser
from e2e_gpu.core.cli_helpers import (e2e_pakage_info, e2e_version_info,
                                      exit_process, manage_exception)
from e2e_gpu.core.config_service import get_user_cred
from e2e_gpu.core.constants import (API_KEY, AUTH_TOKEN, CONFIG, DATASETS,
                                    ENDPOINTS, HELP, IMAGES, MODELS, NOTEBOOK,
                                    PIPELINES, PLANS, PROJECT_ID, PROJECTS,
                                    SKUS, TEAM_ID, TEAMS, USER_INTERRUPTS)
from e2e_gpu.tir.datasets.dataset_parser import parse_dataset_command
from e2e_gpu.tir.datasets.dataset_routing import DatasetRouting
from e2e_gpu.tir.images.image_routing import ImagesRouting
from e2e_gpu.tir.models.model_routing import ModelRouting
from e2e_gpu.tir.notebooks.notebook_routing import NotebookRouting
from e2e_gpu.tir.plans.plan_routing import PlansRouting

# from e2e_gpu.tir.endpoints import plan_to_sku_id
# from e2e_gpu.tir.projects import Projects
# from e2e_gpu.tir.teams import Teams


class CommandsRouting:
    def __init__(self, parser, sub_parser):
        self.parser = parser
        self.sub_parser = sub_parser
        self.arguments = parser.parse_known_args()[0]

    def __call__(self):

        if (self.arguments.version):
            e2e_version_info()

        elif (self.arguments.info):
            e2e_pakage_info()

        elif (self.arguments.help):
            self.parser.print_help()

        elif (self.arguments.command == CONFIG):
            try:
                ConfigParser(self.parser, self.sub_parser).parse()
            except Exception as e:
                manage_exception(e, self.arguments)

        else:
            print(f"Accessing Project : {self.arguments.project}")
            credentials_object = get_user_cred(self.arguments.project)
            tir.init(api_key=credentials_object[API_KEY], access_token=credentials_object[AUTH_TOKEN], 
                     project=credentials_object[PROJECT_ID], team=credentials_object[TEAM_ID])

            command_route_mapping = {DATASETS: DatasetRouting,
                                     ENDPOINTS: "",
                                     IMAGES: ImagesRouting,
                                     MODELS: ModelRouting,
                                     NOTEBOOK: NotebookRouting,
                                     PIPELINES: "",
                                     PLANS: PlansRouting,
                                     PROJECTS: "",
                                     SKUS: "",
                                     TEAMS: ""}

            service_routing = command_route_mapping.get(self.arguments.command)
            service_route = None

            if service_routing:
                service_route = service_routing(self.parser, self.sub_parser)
            else:
                self.parser.print_help()
                exit_process()

            try:
                service_route()
            except USER_INTERRUPTS:
                exit_process()
            except Exception as e:
                manage_exception(e, self.arguments)
