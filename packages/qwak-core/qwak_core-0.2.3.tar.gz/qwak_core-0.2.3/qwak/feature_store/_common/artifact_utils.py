from dataclasses import dataclass, field
from pathlib import Path
from typing import Callable, List, Union

from qwak.clients.feature_store.management_client import FeatureRegistryClient
from qwak.feature_store._common.packaging import upload_artifact
from qwak.feature_store.feature_sets.transformations import BaseTransformation


@dataclass
class ArtifactSpec:
    """
    Dataclass for holding artifacts which will be uploaded
    """

    artifact_name: str
    root_module_path: Path
    artifact_object: Union[BaseTransformation]
    callables: List[Callable] = field(default_factory=lambda: list())
    suffix: str = ""


class ArtifactsUploader:
    @staticmethod
    def upload(artifact: ArtifactSpec) -> str:
        return upload_artifact(
            feature_store_object_name=artifact.artifact_name,
            feature_store_object_name_suffix=artifact.suffix,
            functions=artifact.callables,
            feature_module_dir=artifact.root_module_path,
            features_manager_client=FeatureRegistryClient(),
            artifact_object=artifact.artifact_object,
        )
