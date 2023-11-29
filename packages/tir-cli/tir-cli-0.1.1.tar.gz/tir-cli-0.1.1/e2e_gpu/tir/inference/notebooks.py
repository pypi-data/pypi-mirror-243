from e2enetworks.cloud.tir.notebook import Notebooks

from e2e_gpu.core.cli_helpers import get_output
from e2e_gpu.core.constants import (CONFIRMATION_MSG, CREATE, DEFAULT, DELETE,
                                    GET, HELP, LIST, UPDATE, USER_INTERRUPTS,
                                    YES)
from e2e_gpu.tir.notebooks.constants import START, STOP, UPGRADE
from e2e_gpu.tir.notebooks.notebook_parser import (parse_for_creation,
                                                   parse_for_delete_get_start_stop_request,
                                                   parse_for_upgrade)


class NotebookService:

    def __init__(self, parser, notebook_inputs_parser):
        self.parser = parser
        self.notebook_inputs_parser = notebook_inputs_parser
        self.arguments = None

    def __call__(self, notebook_command):
        operations_set = {CREATE: self.create_notebook,
                          DELETE: self.delete_notebook,
                          GET: self.get_notebook,
                          LIST: self.list_notebook,
                          START: self.start_notebook,
                          STOP: self.stop_notebook,
                          UPGRADE: self.upgrade_notebook_disk}
        operation = operations_set.get(notebook_command)
        if operation:
            operation()

    def create_notebook(self):
        parse_for_creation(self)
        response = Notebooks().create(self.arguments.name, 
                                      self.arguments.plan_name, 
                                      self.arguments.image_id,
                                      self.arguments.disk_size,
                                      self.arguments.notebook_type, 
                                      self.arguments.notebook_url)
        get_output(response)

    def get_notebook(self):
        parse_for_delete_get_start_stop_request(self)
        response = Notebooks().get(self.arguments.notebook_id)
        get_output(response)

    def list_notebook(self):
        response = Notebooks().list()
        get_output(response)

    def delete_notebook(self):
        parse_for_delete_get_start_stop_request(self)
        response = Notebooks().delete(self.arguments.notebook_id)
        get_output(response)
    
    def stop_notebook(self):
        parse_for_delete_get_start_stop_request(self)
        response = Notebooks().stop(self.arguments.notebook_id)
        get_output(response)

    def start_notebook(self):
        parse_for_delete_get_start_stop_request(self)
        response = Notebooks().start(self.arguments.notebook_id)
        get_output(response)

    def upgrade_notebook_disk(self):
        parse_for_upgrade(self)
        response = Notebooks().upgrade(self.arguments.notebook_id, self.arguments.disk_size)
        get_output(response)
   