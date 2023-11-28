from collections import defaultdict
from typing import Dict, List

from _qwak_proto.qwak.data_versioning.data_versioning_pb2 import DataTagSpec
from _qwak_proto.qwak.data_versioning.data_versioning_service_pb2 import (
    GetModelDataTagsRequest,
    GetModelDataTagsResponse,
    RegisterDataTagRequest,
    RegisterDataTagResponse,
)
from _qwak_proto.qwak.data_versioning.data_versioning_service_pb2_grpc import (
    DataVersioningManagementServiceServicer,
)
from qwak_services_mock.mocks.utils.exception_handlers import raise_internal_grpc_error


class DataVersioningServiceMock(DataVersioningManagementServiceServicer):
    def __init__(self):
        super(DataVersioningServiceMock, self).__init__()
        self.tags: Dict[str : List[DataTagSpec]] = defaultdict(list)

    def RegisterDataTag(
        self, request: RegisterDataTagRequest, context
    ) -> RegisterDataTagResponse:
        try:
            self.tags[request.data_tag_spec.build_id].append(request.data_tag_spec)
            return RegisterDataTagResponse()
        except Exception as e:
            raise_internal_grpc_error(context, e)

    def GetModelDataTags(
        self, request: GetModelDataTagsRequest, context
    ) -> GetModelDataTagsResponse:
        try:
            if not request.build_id:
                data_tags_by_model_id = []
                for data_tags_by_build_id in self.tags.values():
                    for data_tag in data_tags_by_build_id:
                        data_tags_by_model_id.append(data_tag)

                return GetModelDataTagsResponse(data_tags=data_tags_by_model_id)
            else:
                data_tags_by_model_id_and_build_id = []
                for data_tags_by_build_id in self.tags[request.build_id]:
                    if data_tags_by_build_id.model_id == request.model_id:
                        data_tags_by_model_id_and_build_id.append(data_tags_by_build_id)

                return GetModelDataTagsResponse(
                    data_tags=data_tags_by_model_id_and_build_id
                )
        except Exception as e:
            raise_internal_grpc_error(context, e)
