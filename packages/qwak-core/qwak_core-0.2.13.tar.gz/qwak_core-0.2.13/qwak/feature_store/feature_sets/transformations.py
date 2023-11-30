import logging
import sys
from abc import ABC, abstractmethod
from typing import Callable, List, Optional

from _qwak_proto.qwak.feature_store.features.feature_set_types_pb2 import (
    KoalasTransformation as ProtoKoalasTransformation,
    SqlTransformation as ProtoSqlTransformation,
    Transformation as ProtoTransformation,
)
from qwak.exceptions import QwakException

logger = logging.getLogger(__name__)


class BaseTransformation(ABC):
    @classmethod
    @abstractmethod
    def _from_proto(cls, proto: ProtoTransformation):
        pass

    @abstractmethod
    def _to_proto(self) -> ProtoTransformation:
        pass

    def get_functions(self) -> Optional[List[Callable]]:
        return None


class BatchTransformation(BaseTransformation, ABC):
    @abstractmethod
    def _to_proto(self, artifact_path: Optional[str] = None) -> ProtoTransformation:
        pass

    @classmethod
    def _from_proto(cls, proto: ProtoTransformation):
        function_mapping = {
            "sql_transformation": SparkSqlTransformation,
            "koalas_transformation": KoalasTransformation,
        }

        function_type: str = proto.WhichOneof("type")
        if function_type in function_mapping:
            function_class = function_mapping.get(function_type)
            return function_class._from_proto(proto)

        raise QwakException(f"Got unsupported function type: {function_type}")


class KoalasTransformation(BatchTransformation):
    """
    Koalas transformation, providing the user with the ability to define a Koalas based UDF for the transformation
    of the FeatureSet. This option will be deprecated in future versions.
    @param function: The Koalas function defined for the transformation
    @type: Callable
    @deprecated
    """

    _artifact_path: Optional[str]

    def __init__(self, function: Callable):
        logger.warning(
            "Koalas transformation is about to be deprecated. "
            "Please use SQL transformation or Pandas based UDFs instead"
        )

        self.function = function
        self._artifact_path = None

    def _validate(self):
        python_major = sys.version_info[0]
        python_minor = sys.version_info[1]
        if f"{python_major}.{python_minor}" != "3.8":
            raise QwakException(
                f"Featurestore UDFs are only supported for python 3.8, instead got: "
                f"{python_major}.{python_minor}"
            )

    def _to_proto(self, artifact_path: Optional[str] = None) -> ProtoTransformation:
        self._validate()

        if artifact_path:
            self._artifact_path = artifact_path

        return ProtoTransformation(
            koalas_transformation=ProtoKoalasTransformation(
                function_name=self.function.__name__
            ),
            artifact_path=self._artifact_path,
        )

    @classmethod
    def _from_proto(cls, proto: "ProtoTransformation"):
        koalas_transformation = proto.koalas_transformation

        return cls(
            function=lambda x: print(
                f"Loading Koalas UDFs is not supported. Can not load {koalas_transformation.function_name}"
            )
        )

    def get_functions(self) -> Optional[List[Callable]]:
        return [self.function]


class SparkSqlTransformation(BatchTransformation):
    """
    A Spark SQL transformation
    :param sql: A valid Spark SQL transformation
    Example transformation:
    ... code-block:: python
        SparkSqlTransformation("SELECT user_id, age FROM data_source")
    """

    def __init__(self, sql):
        self._sql = sql

    @classmethod
    def _from_proto(cls, proto: "ProtoSqlTransformation"):
        return cls(sql=proto.sql_transformation.sql)

    def _to_proto(self, artifact_path: Optional[str] = None) -> ProtoTransformation:
        return ProtoTransformation(
            sql_transformation=ProtoSqlTransformation(sql=self._sql, function_names=[]),
        )


class StreamingTransformation(BaseTransformation, ABC):
    @classmethod
    def _from_proto(cls, proto: "ProtoTransformation"):
        function_mapping = {
            "sql_transformation": SparkSqlTransformation,
        }

        function_type: str = proto.WhichOneof("type")
        if function_type in function_mapping:
            function_class = function_mapping.get(function_type)
            return function_class._from_proto(proto)

        raise QwakException(f"Got unsupported function type: {function_type}")


@abstractmethod
class StructuredStreamingTransformation(StreamingTransformation):
    """
    A structured streaming transformation
    :param sql: A valid Spark structured streaming transformation
    Example transformation:
    ... code-block:: python
        StructuredStreamingTransformation("SELECT user_id, age FROM data_source")
    """

    def __init__(self, sql, functions=None):
        self._sql = sql
        self.functions = functions or []  # TODO: implement

    def _to_proto(self) -> ProtoTransformation:
        return ProtoTransformation(
            sql_transformation=ProtoSqlTransformation(sql=self._sql, function_names=[]),
        )
