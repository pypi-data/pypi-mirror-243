from ai.h2o.featurestore.api.v1.CoreService_pb2_grpc import CoreServiceStub

from .base_job import BaseJob
from .ml_dataset import MLDataset


class CreateMLDatasetJob(BaseJob):
    def __init__(self, stub: CoreServiceStub, rest_stub, job_id):
        super().__init__(stub, job_id)
        self._rest_stub = rest_stub

    def _response_method(self, job_id):
        return MLDataset(self._stub, self._rest_stub, self._stub.GetMLDatasetCreationJobOutput(job_id))
