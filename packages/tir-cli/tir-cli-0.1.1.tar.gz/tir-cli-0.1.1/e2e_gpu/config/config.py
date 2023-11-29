import json
import os

from e2e_gpu.core.cli_helpers import exit_process
from e2e_gpu.core.config_service import get_user_cred, is_valid, system_file
from e2e_gpu.core.constants import (ALIAS, API_KEY, AUTH_TOKEN, DEFAULT,
                                    PROJECT_ID, TEAM_ID)


class AuthConfig:
    def __init__(self, **kwargs):
        self.kwargs = kwargs
        self.system_type, self.folder, self.config_file = system_file()

    def _windows_hider(self):
        os.system("attrib +h " + self.folder)

    def _windows_file_check(self):
        if not os.path.isdir(self.folder):
            return -1
        else:
            self._windows_hider()
            return 1 if os.path.isfile(self.config_file) else 0

    def _linux_mac_file_check(self):
        if not os.path.isdir(self.folder):
            return -1
        else:
            return 1 if os.path.isfile(self.config_file) else 0

    def _check_if_file_exist(self):
        '''returns 1 if file exist,
            returns 0 if folder exist,
            returns -1 if both not found'''
        if self.system_type == "Windows":
            return self._windows_file_check()
        elif self.system_type == "Linux" or self.system_type == "Darwin":
            return self._linux_mac_file_check()

    def add_to_config(self):
        file_exist_check = self._check_if_file_exist()
        if file_exist_check != 1:
            self._create_new_file() if file_exist_check == 0 else os.mkdir(self.folder), self._create_new_file()
        self._add_json_to_file()

    def delete_from_config(self, x=0):
        file_exist_check = self._check_if_file_exist()
        if file_exist_check == -1 | file_exist_check == 0:
            exit_process("You need to add your projects/credentials first, for more 'tir config -h' ")

        elif file_exist_check == 1:
            with open(self.config_file, 'r+') as file_reference:
                file_contents_object = json.loads(file_reference.read())
                delete_output = file_contents_object.pop(
                    self.kwargs["project"], None)
                self._check_and_delete_for_default(file_contents_object)

                if delete_output == None and x != 1:
                    exit_process("No such alias found. Please re-check and enter again")
                else:
                    file_reference.seek(0)
                    file_reference.write(json.dumps(file_contents_object))
                    file_reference.truncate()
                    if (x != 1):
                        print("Project/Token Successfully deleted")

    def _check_and_delete_for_default(self, file_contents_object):
        try:
            if self.kwargs["project"] == file_contents_object[DEFAULT][API_KEY]:
                file_contents_object.pop(DEFAULT, None)
        except:
            pass

    def _create_new_file(self):
        with open(self.config_file, 'w'):
            pass

    def _add_json_to_file(self):
        api_access_credentials_object = self._read_config_file()
        if api_access_credentials_object is None:
            exit_process("Invalid credentials given please re-check")

        if (is_valid(api_access_credentials_object[API_KEY], api_access_credentials_object[AUTH_TOKEN])):
            with open(self.config_file, 'r+') as file_reference:
                read_string = file_reference.read()
                if read_string == "":
                    file_reference.write(json.dumps({self.kwargs[ALIAS]:
                                                     api_access_credentials_object}))
                else:
                    api_access_credentials = json.loads(read_string)
                    api_access_credentials.update({self.kwargs[ALIAS]:
                                                   api_access_credentials_object})
                    file_reference.seek(0)
                    file_reference.write(json.dumps(api_access_credentials))
            print("Project/Token successfully added")
        else:
            exit_process("Invalid credentials given please re-check")

    def _read_config_file(self):
        path = input("input the file path : ")

        # for drag and drop
        if (path[0] == "'" and path[-1] == "'"):
            path = path.lstrip(path[0])
            path = path.rstrip(path[-1])

        if ((path.endswith("/config.json") or path == "config.json") and os.path.isfile(path)):
            with open(path, 'r+') as file_reference:
                file_contents_object = json.loads(file_reference.read())
                try:
                    file_contents_object[API_KEY], file_contents_object[AUTH_TOKEN], file_contents_object[PROJECT_ID], file_contents_object[TEAM_ID]
                    return file_contents_object
                except:
                    return None

    def set_default(self):
        api_access_credentials_object = {API_KEY: self.kwargs["project"],
                                         AUTH_TOKEN: self.kwargs["project"],
                                         PROJECT_ID: self.kwargs["project"],
                                         TEAM_ID: self.kwargs["project"]}
        with open(self.config_file, 'r+') as file_reference:
            read_string = file_reference.read()
            if read_string == "":
                file_reference.write(json.dumps({DEFAULT:
                                                 api_access_credentials_object}))
            else:
                api_access_credentials = json.loads(read_string)
                api_access_credentials.update({DEFAULT:
                                               api_access_credentials_object})
                file_reference.seek(0)
                file_reference.truncate(0)
                file_reference.write(json.dumps(api_access_credentials))
