from e2enetworks.cloud.tir.models import Models

from e2e_gpu.core.cli_helpers import get_output
from e2e_gpu.core.constants import (CONFIRMATION_MSG, CREATE, DEFAULT, DELETE,
                                    GET, HELP, LIST, UPDATE, USER_INTERRUPTS,
                                    YES)
from e2e_gpu.tir.models.constants import DOWNLOAD_MODEL, PUSH_MODEL
from e2e_gpu.tir.models.model_parser import (parse_for_creation,
                                             parse_for_deletion,
                                             parse_for_get_info,
                                             parse_for_model_download,
                                             parse_for_model_upload)


class ModelService:

    def __init__(self, parser, model_inputs_parser):
        self.parser = parser
        self.model_inputs_parser = model_inputs_parser
        self.arguments = None

    def __call__(self, model_command):
        operations_set = {CREATE: self.create_model,
                          DELETE: self.delete_model,
                          GET: self.get_model,
                          LIST: self.list_model,
                          PUSH_MODEL: self.upload_model_to_storage,
                          DOWNLOAD_MODEL: self.download_model_from_storage}
        operation = operations_set.get(model_command)
        if operation:
            operation()

    def create_model(self):
        parse_for_creation(self)
        response = Models().create(name=self.arguments.name, 
                                   storage_type=self.arguments.storage_type)
        get_output(response)

    def get_model(self):
        parse_for_get_info(self)
        response = Models().get(self.arguments.model_id)
        get_output(response)

    def list_model(self):
        response = Models().list()
        get_output(response)

    def delete_model(self):
        parse_for_deletion(self)
        response = Models().delete(self.arguments.model_id)
        get_output(response)

    def upload_model_to_storage(self):
        parse_for_model_upload(self)
        response = Models().push_model(self.arguments.model_path,
                                       prefix=self.arguments.prefix,
                                       model_id=self.arguments.model_id)
        get_output(response)

    def download_model_from_storage(self):
        parse_for_model_download(self)
        response = Models().download_model(model_id=self.arguments.model_id,
                                           local_path=self.arguments.local_path,
                                           prefix=self.arguments.prefix)
        get_output(response)
