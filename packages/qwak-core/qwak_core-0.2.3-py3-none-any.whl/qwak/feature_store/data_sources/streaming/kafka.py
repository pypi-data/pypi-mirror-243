from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from enum import Enum
from typing import Dict, Optional, Type

from _qwak_proto.qwak.feature_store.sources.data_source_pb2 import (
    DataSourceSpec as ProtoDataSourceSpec,
)
from _qwak_proto.qwak.feature_store.sources.streaming_pb2 import (
    Authentication as ProtoAuthentication,
    Deserialization as ProtoDeserialization,
    GenericDeserializer as ProtoGenericDeserializer,
    KafkaSourceV1 as ProtoKafkaSourceV1,
    MessageFormat as ProtoMessageFormat,
    Plain as ProtoPlain,
    Ssl as ProtoSsl,
    StreamingSource as ProtoStreamingSource,
)
from qwak.exceptions import QwakException
from qwak.feature_store.data_sources.streaming._streaming import BaseStreamingSource


@dataclass
class BaseAuthentication(ABC):
    @abstractmethod
    def to_proto(self) -> ProtoAuthentication:
        pass

    @classmethod
    def from_proto(cls, proto):
        pass


@dataclass
class PlainAuthentication(BaseAuthentication):
    def to_proto(self) -> ProtoAuthentication:
        return ProtoAuthentication(plain_configuration=ProtoPlain())

    @classmethod
    def from_proto(cls, proto):
        return cls()


@dataclass
class SslAuthentication(BaseAuthentication):
    def to_proto(self) -> ProtoAuthentication:
        return ProtoAuthentication(ssl_configuration=ProtoSsl())

    @classmethod
    def from_proto(cls, proto):
        return cls()


class Deserialization(ABC):
    @abstractmethod
    def _to_proto(self) -> ProtoDeserialization:
        pass


class MessageFormat(Enum):
    JSON = ProtoMessageFormat.JSON
    AVRO = ProtoMessageFormat.AVRO


@dataclass
class GenericDeserializer(Deserialization):
    message_format: MessageFormat
    schema: str

    def _to_proto(self) -> ProtoDeserialization:
        # TODO: add backend schema validation
        return ProtoDeserialization(
            generic_deserializer=ProtoGenericDeserializer(
                deserializer_format=self.message_format.value, schema=self.schema
            )
        )


@dataclass
class KafkaSource(BaseStreamingSource):
    bootstrap_servers: str

    # Deserialization
    deserialization: Deserialization

    # secret configs, the value is resolved to the secret,
    # s.t. (key, value) -> (key, get_secret(value))
    # not all configs will be respected, this is a best-effort
    secret_configs: Dict[str, str] = field(default_factory=lambda: {})

    # passthrough configs - not all configs will be respected,
    # this is a best-effort
    passthrough_configs: Dict[str, str] = field(default_factory=lambda: {})

    # the following 3 are pairwise mutually exclusive
    assign: Optional[str] = None
    subscribe: Optional[str] = None
    subscribe_pattern: Optional[str] = None

    authentication_method: Optional[BaseAuthentication] = field(
        default_factory=lambda: SslAuthentication()
    )

    def __post_init__(self):
        self._validate()

    def _validate(self):
        num_defined = len(
            [
                _
                for _ in [self.assign, self.subscribe, self.subscribe_pattern]
                if _ is not None
            ]
        )
        if num_defined != 1:
            raise QwakException(
                "Exactly one of (assign, subscribe, subscribe_pattern) must be defined!"
            )

    def _to_proto(self) -> ProtoDataSourceSpec:
        return ProtoDataSourceSpec(
            stream_source=ProtoStreamingSource(
                name=self.name,
                description=self.description,
                kafkaSourceV1=ProtoKafkaSourceV1(
                    bootstrap_servers=self.bootstrap_servers,
                    assign=self.assign,
                    subscribe=self.subscribe,
                    subscribe_pattern=self.subscribe_pattern,
                    secret_configs=self.secret_configs,
                    passthrough_configs=self.passthrough_configs,
                    authentication_method=self.authentication_method.to_proto(),
                    deserialization=self.deserialization._to_proto(),
                ),
            )
        )

    @classmethod
    def _from_proto(cls, proto) -> Type["KafkaSource"]:
        def _proto_to_authentication_mapper(
            proto_authentication_method: ProtoAuthentication,
        ) -> BaseAuthentication:
            proto_authentication_method = getattr(
                proto_authentication_method,
                proto_authentication_method.WhichOneof("type"),
            )
            if isinstance(proto_authentication_method, ProtoPlain):
                return PlainAuthentication.from_proto(proto_authentication_method)
            elif isinstance(proto_authentication_method, ProtoSsl):
                return SslAuthentication.from_proto(proto_authentication_method)
            else:
                raise QwakException(
                    f"Got unsupported authentication method {proto_authentication_method}"
                )

        def proto_to_deserializer_mapper(
            proto_deserialization: ProtoDeserialization,
        ) -> Deserialization:
            deserializer = getattr(
                proto_deserialization, proto_deserialization.WhichOneof("type")
            )

            if isinstance(deserializer, ProtoGenericDeserializer):
                return GenericDeserializer(
                    message_format=list(MessageFormat)[
                        deserializer.deserializer_format - 1
                    ],
                    schema=deserializer.schema,
                )

            else:
                raise QwakException(f"Got unsupported deserializer type {deserializer}")

        kafka = proto.kafkaSourceV1
        topic_configuration_key = kafka.WhichOneof("topic_configuration")
        oneof_args = {topic_configuration_key: getattr(kafka, topic_configuration_key)}
        return cls(
            name=proto.name,
            description=proto.description,
            bootstrap_servers=kafka.bootstrap_servers,
            secret_configs=kafka.secret_configs,
            passthrough_configs=kafka.passthrough_configs,
            deserialization=proto_to_deserializer_mapper(kafka.deserialization),
            authentication_method=_proto_to_authentication_mapper(
                kafka.authentication_method
            ),
            **oneof_args,
        )
