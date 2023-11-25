<!--suppress HtmlDeprecatedAttribute -->
<div align=center>
  <h1>Cloud Eventful</h1>
  <h3>Broker agnostic library to associate JSON Schemas to message broker topics.</h3>
  <img src="https://img.shields.io/badge/License-MIT-blue.svg"
   height="20"
   alt="License: MIT">
  <img src="https://img.shields.io/badge/code%20style-black-000000.svg"
   height="20"
   alt="Code style: black">
  <img src="https://img.shields.io/pypi/v/cloudeventful.svg"
   height="20"
   alt="PyPI version">
  <img src="https://img.shields.io/badge/coverage-100%25-success"
   height="20"
   alt="Code Coverage">
</div>

## Install

Cloud Eventful is on PyPI and can be installed with:

```shell
poetry add cloudeventful
```

or

```shell
pip install cloudeventful
```

## Usage

This library provides a `CloudEventful` class which can be used to generate
[CloudEvents](https://cloudevents.io/) and associate
[Pydantic](https://pydantic-docs.helpmanual.io/) models as the cloud event `data` field
on a per-topic basis.

### Model Registration

A model is associated with a pattern describing the topics it may be published to using
the `data_model` decorator.

```python
import re

from cloudeventful import CloudEventful
from pydantic import BaseModel

ce = CloudEventful(api_version="1.0.0", default_source="my/event/server")


@ce.data_model(re.compile(r"/.*/coffee"))
class Coffee(BaseModel):
    flavor: str
```

### Cloud Event Generation

Once data models are registered, CloudEvent objects can be generated with an instance of
the generated model as the CloudEvent `data` property.

```pycon
>>> ce.event(Coffee(flavor="mocha"))
CloudEvent[ModelType](id='9b21a718-9dc1-4b56-a4ea-4e9911bc8ca6', source='my/event/server', specversion='1.0', type='Coffee', data=Coffee(flavor='mocha'), datacontenttype='application/json', dataschema='/Coffee', subject='Coffee', time=datetime.datetime(2022, 11, 19, 15, 33, 6, 39795))
```

### Publish

A publish function can be registered with a `CloudEventful` instance to enforce topic
integrity at run time. This is done by setting the `publish_function` property on a
`CloudEventful` instance.

A publish function must accept at least a topic arg as a str and a data arg as a
registered data model.

Then, the `CloudEventful` publish function can be used to wrap data models in a
CloudEvent and publish them as JSON strings. Keyword args will be passed to the
registered publish function.

## Example using MQTT with Paho

```python
import re

from cloudeventful import CloudEventful
import paho.mqtt.client as mqtt
from pydantic import BaseModel

server_id = "my/event/server"

client = mqtt.Client(server_id)
client.connect("127.0.0.1")

ce = CloudEventful(
    api_version="1.0.0",
    default_source=server_id,
    publish_function=client.publish,
    default_topic_factory=lambda m: f"/api/v1/{type(m).__name__.lower()}"
)


@ce.data_model(re.compile(r"/.*/coffee"))
class Coffee(BaseModel):
    flavor: str


@ce.data_model(re.compile(r"/.*/pen"))
class Pen(BaseModel):
    color: str


# Publish a data model wrapped in a cloud event.
ce.publish(Coffee(flavor="mocha"))
# Raise `ValueError` because topic does not match pattern of this model.
ce.publish(Pen(color="black"), topic="wrong-topic")
```

## Support The Developer

<a href="https://www.buymeacoffee.com/mburkard" target="_blank">
  <img src="https://cdn.buymeacoffee.com/buttons/v2/default-blue.png"
       width="217"
       height="60"
       alt="Buy Me A Coffee">
</a>
