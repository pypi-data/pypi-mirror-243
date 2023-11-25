"""Provides the `CloudEventful` class for declaring event models."""
from __future__ import annotations

import datetime
import re
from typing import Any, AnyStr, Callable, Generic, Pattern, Protocol, Type, TypeVar
from uuid import uuid4

from pydantic import BaseModel
from pydantic.generics import GenericModel

from cloudeventful import CloudEvent
from cloudeventful._cloud_event_doc import CloudEventDoc

__all__ = ("CloudEventful", "EventMetadata")

ModelType = TypeVar("ModelType", bound=BaseModel)


def _uuid(_model: BaseModel) -> str:
    return str(uuid4())


def _schema(model: Type[ModelType]) -> str:
    return f"/{model.__name__}"


def _type(model: BaseModel) -> str:
    return type(model).__name__


class _PublishFunctionType(Protocol):
    def __call__(self, topic: str, data: str, **kwargs: Any) -> None:
        """Protocol function signature."""


class EventMetadata(GenericModel, Generic[ModelType]):
    """Registered event metadata."""

    model_type: Type[ModelType]
    topic_pattern: str
    id_factory: Callable[[ModelType], str] | None = None
    source: str | None = None
    specversion: str | None = None
    type_factory: Callable[[ModelType], str] | None = None
    datacontenttype: str | None = None
    dataschema_factory: Callable[[ModelType], str] | None = None
    subject_factory: Callable[[ModelType], str] | None = None
    time_factory: Callable[[], datetime.datetime] | None = None
    topic_factory: Callable[[ModelType], str] | None = None


class CloudEventful:
    """Manager to register on instantiate event models."""

    def __init__(
        self,
        api_version: str,
        default_source: str,
        default_id_factory: Callable[[ModelType], str] = _uuid,
        default_specversion: str = "1.0",
        default_type_factory: Callable[[ModelType], str] = _type,
        default_datacontenttype: str = "application/json",
        default_dataschema_factory: Callable[[Type[ModelType]], str] = _schema,
        default_subject_factory: Callable[[ModelType], str] | None = None,
        default_time_factory: Callable[[], datetime.datetime] = datetime.datetime.now,
        publish_function: _PublishFunctionType | None = None,
        default_topic_factory: Callable[[ModelType], str] | None = None,
    ) -> None:
        """Init event manager with default args for generated events.

        :param default_id_factory: Callable to produce default value for
            event id, defaults to a UUID string.
        :param default_source: Default event source.
        :param default_specversion: Default event specversion.
        :param default_type_factory: Callable to produce default value
            for type.
        :param default_datacontenttype: Default event datacontenttype,
            defaults to "application/json".
        :param default_dataschema_factory: Callable to produce default
            value for dataschema, default is `f"/{model.__name__}"`.
        :param default_subject_factory: Callable to produce default
            value for subject.
        :param default_time_factory: Callable to produce default value
            for time.
        :param publish_function: Function to publish a data model wrapped
            in a `CloudEvent`.
        :param default_topic_factory: Function to generate topic value
            from a model instance for the `publish` function.
        """
        self._api_version = api_version
        self._default_source = default_source
        self._default_id_factory = default_id_factory
        self._default_specversion = default_specversion
        self._default_type_factory = default_type_factory
        self._default_datacontenttype = default_datacontenttype
        self._default_dataschema_factory = default_dataschema_factory
        self._default_subject_factory = default_subject_factory
        self._default_time_factory = default_time_factory
        self._data_models: dict[Type[BaseModel], EventMetadata] = {}
        self._patterns: dict[str | bytes, Type[BaseModel]] = {}
        self._default_topic_factory = default_topic_factory
        self.publish_function = publish_function

    @property
    def api_version(self) -> str:
        """Get version of the API publishing data models."""
        return self._api_version

    @api_version.setter
    def api_version(self, api_version: str) -> None:
        """Set version of the API publishing data models."""
        self._api_version = api_version

    @property
    def default_id_factory(self) -> Callable[[ModelType], str]:
        """Get default callable for generating `CloudEvent` ids."""
        return self._default_id_factory

    @default_id_factory.setter
    def default_id_factory(
        self, default_id_factory: Callable[[ModelType], str]
    ) -> None:
        """Set default callable for generating `CloudEvent` ids."""
        self._default_id_factory = default_id_factory

    @property
    def default_source(self) -> str:
        """Get default `CloudEvent` source."""
        return self._default_source

    @default_source.setter
    def default_source(self, default_source: str) -> None:
        """Set default `CloudEvent` source."""
        self._default_source = default_source

    @property
    def default_specversion(self) -> str:
        """Get default `CloudEvent` specversion."""
        return self._default_specversion

    @default_specversion.setter
    def default_specversion(self, default_specversion: str) -> None:
        """Set default `CloudEvent` specversion."""
        self._default_specversion = default_specversion

    @property
    def default_type_factory(self) -> Callable[[ModelType], str]:
        """Get default callable for generating `CloudEvent` type."""
        return self._default_type_factory

    @default_type_factory.setter
    def default_type_factory(
        self, default_type_factory: Callable[[ModelType], str]
    ) -> None:
        """Set default callable for generating `CloudEvent` type."""
        self._default_type_factory = default_type_factory

    @property
    def default_datacontenttype(self) -> str:
        """Get default `CloudEvent` datacontenttype."""
        return self._default_datacontenttype

    @default_datacontenttype.setter
    def default_datacontenttype(self, default_datacontenttype: str) -> None:
        """Set default `CloudEvent` datacontenttype."""
        self._default_datacontenttype = default_datacontenttype

    @property
    def default_dataschema_factory(self) -> Callable[[Type[ModelType]], str]:
        """Get default callable for generating `CloudEvent` dataschema."""
        return self._default_dataschema_factory

    @default_dataschema_factory.setter
    def default_dataschema_factory(
        self, default_dataschema_factory: Callable[[Type[ModelType]], str]
    ) -> None:
        """Set default callable for generating `CloudEvent` dataschema."""
        self._default_dataschema_factory = default_dataschema_factory

    @property
    def default_subject_factory(self) -> Callable[[ModelType], str] | None:
        """Get default callable for generating `CloudEvent` subject."""
        return self._default_subject_factory

    @default_subject_factory.setter
    def default_subject_factory(
        self, default_subject_factory: Callable[[ModelType], str] | None
    ) -> None:
        """Set default callable for generating `CloudEvent` subject."""
        self._default_subject_factory = default_subject_factory

    @property
    def default_time_factory(self) -> Callable[[], datetime.datetime]:
        """Get default callable for generating `CloudEvent` time."""
        return self._default_time_factory

    @default_time_factory.setter
    def default_time_factory(
        self, default_time_factory: Callable[[], datetime.datetime]
    ) -> None:
        """Set default callable for generating `CloudEvent` time."""
        self._default_time_factory = default_time_factory

    @property
    def publish_function(self) -> _PublishFunctionType | None:
        """Get the publish function."""
        return self._publish_function

    @publish_function.setter
    def publish_function(self, publish_function: _PublishFunctionType | None) -> None:
        """Set the publish function."""
        self._publish_function = publish_function

    @property
    def default_topic_factory(self) -> Callable[[ModelType], str] | None:
        """Get default callable for determining publish topic."""
        return self._default_topic_factory

    @default_topic_factory.setter
    def default_topic_factory(
        self, default_topic_factory: Callable[[ModelType], str] | None
    ) -> None:
        """Set default callable for determining publish topic."""
        self._default_topic_factory = default_topic_factory

    def publish(
        self,
        data: ModelType,
        topic: str | None = None,
        id_: str | None = None,
        source: str | None = None,
        specversion: str | None = None,
        type_: str | None = None,
        datacontenttype: str | None = None,
        dataschema: str | None = None,
        subject: str | None = None,
        time: datetime.datetime | None = None,
        **kwargs: Any,
    ) -> None:
        """Publish a message with the pre-configured `publish_function`.

        The data model will be wrapped in a `CloudEvent` object.

        :param data: Data model to publish.
        :param topic: Topic to publish message to.
        :param id_: `CloudEvent` id.
        :param source: `CloudEvent` source.
        :param specversion: `CloudEvent` specversion.
        :param type_: `CloudEvent` type.
        :param datacontenttype: `CloudEvent` datacontenttype.
        :param dataschema: `CloudEvent` dataschema.
        :param subject: `CloudEvent` subject.
        :param time: `CloudEvent` time.
        :param kwargs: Any kwargs to be passed to the publish function.
        :return: None.
        """
        if self.publish_function is None:
            raise RuntimeError("Publish function has not been set.")

        metadata = self._data_models[type(data)]
        if topic is None:
            topic_factory = self.default_topic_factory or metadata.topic_factory
            if not topic_factory:
                msg = (
                    f"Topic factory for {type(data).__name__} has not been set and no"
                    f" topic was provided to publish."
                )
                raise RuntimeError(msg)
            topic = topic_factory(data)

        pattern = metadata.topic_pattern
        if not re.match(pattern, topic):
            msg = f"{topic} does not match pattern {pattern}."
            raise ValueError(msg)
        event = self.event(
            model=data,
            id_=id_,
            source=source,
            specversion=specversion,
            type_=type_,
            datacontenttype=datacontenttype,
            dataschema=dataschema,
            subject=subject,
            time=time,
        )
        self.publish_function(topic, event.model_dump_json(), **kwargs)

    def data_model(
        self,
        topic_pattern: Pattern[AnyStr],
        id_factory: Callable[[ModelType], str] | None = None,
        source: str | None = None,
        specversion: str | None = None,
        type_factory: Callable[[ModelType], str] | None = None,
        datacontenttype: str | None = None,
        dataschema_factory: Callable[[ModelType], str] | None = None,
        subject_factory: Callable[[ModelType], str] | None = None,
        time_factory: Callable[[], datetime.datetime] | None = None,
        topic_factory: Callable[[ModelType], str] | None = None,
    ) -> Callable[[Type[ModelType]], Type[ModelType]]:
        """Decorate a data model as event data.

        The factory parameters will produce values for the generated
        cloud event on event creation.

        :param topic_pattern: Regex describing what topics this data
            model is published to.
        :param id_factory: Callable to produce id.
        :param source: Default event source.
        :param specversion: Default event specversion.
        :param type_factory: Callable to produce default type.
        :param datacontenttype: Callable to produce datacontenttype.
        :param dataschema_factory: Callable to produce dataschema.
        :param subject_factory: Callable to produce subject.
        :param time_factory: Callable to produce time.
        :param topic_factory: Callable to produce topic when published.
        :return: The decorated model.
        """

        def _wrapper(model_type: Type[ModelType]) -> Type[ModelType]:
            if duplicate := self._patterns.get(topic_pattern.pattern):
                msg = (
                    f'Pattern "{topic_pattern.pattern!r}" duplicated for'
                    f' "{model_type.__name__}" and'
                    f' "{duplicate.__name__}".'  # type: ignore
                )
                raise ValueError(msg)
            self._patterns[topic_pattern.pattern] = model_type
            self._data_models[model_type] = EventMetadata[ModelType](
                model_type=model_type,
                topic_pattern=topic_pattern.pattern,
                id_factory=id_factory,
                source=source,
                specversion=specversion,
                type_factory=type_factory,
                datacontenttype=datacontenttype,
                dataschema_factory=dataschema_factory,
                subject_factory=subject_factory,
                time_factory=time_factory,
                topic_factory=topic_factory,
            )
            return model_type

        return _wrapper

    def discover(self) -> CloudEventDoc:
        """Get a `CloudEventDoc` describing registered data models."""
        return CloudEventDoc(
            api_version=self._api_version,
            data_models={
                e.topic_pattern: e.model_type.model_json_schema()
                for e in self._data_models.values()
            },
        )

    def event(
        self,
        model: ModelType,
        id_: str | None = None,
        source: str | None = None,
        specversion: str | None = None,
        type_: str | None = None,
        datacontenttype: str | None = None,
        dataschema: str | None = None,
        subject: str | None = None,
        time: datetime.datetime | None = None,
    ) -> CloudEvent[ModelType]:
        """Generate event for a model.

        If event parameters are not provided factory methods will be
        used.

        :param model: The model that the event data.
        :param id_: Cloud event id.
        :param source: Cloud event source.
        :param specversion: Cloud event specversion.
        :param type_: Cloud event type.
        :param datacontenttype: Cloud event datacontenttype.
        :param dataschema: Cloud event dataschema.
        :param subject: Cloud event subject.
        :param time: Cloud event time.
        :return: A cloud event with the provided model as data.
        """
        metadata = self._data_models[type(model)]
        event = CloudEvent[ModelType](
            id=id_ or (metadata.id_factory or self.default_id_factory)(model),
            source=source or metadata.source or self.default_source,
            specversion=specversion or metadata.specversion or self.default_specversion,
            type=type_ or (metadata.type_factory or self.default_type_factory)(model),
            datacontenttype=datacontenttype
            or metadata.datacontenttype
            or self.default_datacontenttype,
            dataschema=dataschema
            or (metadata.dataschema_factory or self.default_dataschema_factory)(
                type(model)
            ),
            subject=subject
            or (
                metadata.subject_factory
                or self.default_subject_factory
                or (lambda _m: type(model).__name__)
            )(model),
            time=time or (metadata.time_factory or self.default_time_factory)(),
            data=model,
        )
        if self.default_datacontenttype is not None:
            event.datacontenttype = self.default_datacontenttype
        if self.default_subject_factory is not None:
            event.subject = self.default_subject_factory(model)
        if self.default_time_factory is not None:
            event.time = self.default_time_factory()
        return event
