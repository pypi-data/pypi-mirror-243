import json
import os
import platform

from e2e_gpu.core.cli_helpers import exit_process
from e2e_gpu.core.constants import (API_KEY, AUTH_TOKEN, DEFAULT,
                                    INVALID_PROJECT, PROJECT_ID, TEAM_ID)
from e2e_gpu.core.request_service import Methods, Request

__NIX_SYSTEM = ["Linux", "Darwin"]
__WINDOWS = "Windows"
__TIR_FOLDER = ".TIR_CLI"
__TIR_CONFIG = "config.json"


def system_file():
    home_directory = os.path.expanduser("~")
    if platform.system() == __WINDOWS:
        return __WINDOWS, f"{home_directory}\{__TIR_FOLDER}", f"{home_directory}\{__TIR_FOLDER}\{__TIR_CONFIG}"
    elif platform.system() in __NIX_SYSTEM:
        return platform.system(), f"{home_directory}/{__TIR_FOLDER}", f"{home_directory}/{__TIR_FOLDER}/{__TIR_CONFIG}"


def is_valid(api_key, auth_token):
    url = "api/v1/customer/details/?apikey=" + api_key+"&contact_person_id=null"
    response = Request(url, auth_token, {}, Methods.GET).make_api_call()
    if ('code' in response):
        return True
    else:
        return False


def get_user_cred(name, type=0):
    ''' type = 0 default case get credentials object,
        type = 1 fetch all projects/token list'''

    system_type, folder, config_file = system_file()
    try:
        f = open(config_file)
        credentials = json.load(f)
        f.close()
    except Exception as e:
        exit_process(e)

    # listing projects
    if (name == "all" and type == 1):
        return credentials.keys()

    # getting/checking projects
    try:
        if name == DEFAULT:
            name = credentials[name]['auth_token']
        credentials[name][AUTH_TOKEN], credentials[name][API_KEY], credentials[name][PROJECT_ID], credentials[name][TEAM_ID]
        return credentials[name]
    except:
        exit_process(INVALID_PROJECT)
