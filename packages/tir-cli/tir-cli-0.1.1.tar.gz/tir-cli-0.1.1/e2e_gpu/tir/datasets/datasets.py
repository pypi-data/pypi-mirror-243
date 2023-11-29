from e2enetworks.cloud.tir.datasets import Datasets

from e2e_gpu.core.cli_helpers import get_output
from e2e_gpu.core.constants import (CONFIRMATION_MSG, CREATE, DEFAULT, DELETE,
                                    GET, HELP, LIST, UPDATE, USER_INTERRUPTS,
                                    YES)
from e2e_gpu.tir.datasets.constants import DOWNLOAD_DATASET, PUSH_DATASET
from e2e_gpu.tir.datasets.dataset_parser import (parse_for_creation,
                                                 parse_for_dataset_download,
                                                 parse_for_dataset_upload,
                                                 parse_for_deletion,
                                                 parse_for_get_info)


class DatasetService:

    def __init__(self, parser, dataset_inputs_parser):
        self.parser = parser
        self.dataset_inputs_parser = dataset_inputs_parser
        self.arguments = None

    def __call__(self, dataset_command):
        operations_set = {CREATE: self.create_dataset,
                          DELETE: self.delete_dataset,
                          GET: self.get_dataset,
                          LIST: self.list_dataset,
                          DOWNLOAD_DATASET: self.download_dataset,
                          PUSH_DATASET: self.upload_dataset}
        operation = operations_set.get(dataset_command)
        if operation:
            operation()

    def create_dataset(self):
        parse_for_creation(self)
        response = Datasets().create(name=self.arguments.name, bucket_type=self.arguments.bucket_type)
        get_output(response)

    def get_dataset(self):
        parse_for_get_info(self)
        response = Datasets().get(self.arguments.dataset_id)
        get_output(response)

    def list_dataset(self):
        response = Datasets().list()
        get_output(response)

    def delete_dataset(self):
        parse_for_deletion(self)
        response = Datasets().delete(self.arguments.dataset_id)
        get_output(response)
    
    def download_dataset(self):
        parse_for_dataset_download(self)
        Datasets().download_dataset(dataset_id=self.arguments.dataset_id,
                                               local_path=self.arguments.local_path,
                                               prefix=self.arguments.prefix)

    def upload_dataset(self):
        parse_for_dataset_upload(self)
        Datasets().upload_dataset(dataset_id=self.arguments.dataset_id,
                                             dataset_path=self.arguments.dataset_path,
                                             prefix=self.arguments.prefix)
