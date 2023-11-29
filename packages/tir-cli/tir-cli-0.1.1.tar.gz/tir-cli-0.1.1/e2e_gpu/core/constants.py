# version
PACKAGE_VERSION = "tir-cli/1.0.0 Python Linux/Mac/Windows"

# package_info
PACKAGE_INFO = " A command line tool developed by E2E Networks Ltd. \n Used to access and manage TIR AI-ML services from cmd/shell \n Published 1st Dec 2023"

# urls
BASE_URL = "https://api.e2enetworks.com/myaccount/"

# name
TIR_CLI = "tir"

# command names
CONFIG = "config"
DATASETS = "datasets"
IMAGES = "images"
MODELS = "models"
NOTEBOOK = "notebook"
PIPELINES = "pipelines"
PLANS = "plans"
PROJECTS = "projects"
SKUS = "skus"
TEAMS = "teams"
ENDPOINTS = "endpoints"
HELP = "--help"

# crud operations
CREATE = "create"
LIST = "list"
GET = "get"
UPDATE = "update"
DELETE = "delete"

# config keys
AUTH_TOKEN = "auth_token"
API_KEY = "api_key"
PROJECT_ID = "project_id"
TEAM_ID = "team_id"

# messages
VALID_PROJECT = "Valid alias"
INVALID_PROJECT = "Warning : The given project/credential doesn't exist"
CONFIRMATION_MSG = "are you sure you want to proceed, press y for yes, else any other key : "
ERROR_MSG = "Oops!! an unforseen error occured, please try again with --debug flag or contact us"

# errors and Interrupts
USER_INTERRUPTS = (KeyboardInterrupt, EOFError)

# keys
DEFAULT = "default"
ALIAS = "alias"
YES = "y"
RESERVES = [CONFIG, DATASETS, IMAGES, NOTEBOOK, PIPELINES,
            PROJECTS, SKUS, TEAMS, ENDPOINTS, VALID_PROJECT, INVALID_PROJECT]
