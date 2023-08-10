import ast
import base64
import enum

from translation.language import Language
from translation.text import Text


_EVENT_SOURCE_KEYS = (
    "EventSource",
    "eventSource"
)


@enum.unique
class EventType(enum.Enum):
    SNS = enum.auto()
    SQS = enum.auto()
    KINESIS = enum.auto()
    CUSTOM = enum.auto()

    @classmethod
    def from_string(cls, name):
        return getattr(cls, name.upper(), EventType.CUSTOM)


def lambda_handler(event, translator):
    texts = _texts_from(event)
    translations = translator.translate_many(texts)

    return [
        (t.body, tr if isinstance(tr, str) else None)
        for t, tr in zip(texts, translations)
    ]


def _texts_from(event):
    t = _determine_type_of(event)

    text_from = (
        _text_from_sns
        if t is EventType.SNS
        else _text_from_sqs
        if t is EventType.SQS
        else _text_from_kinesis
        if t is EventType.KINESIS
        else _text_from_custom_event
    )

    texts = text_from(event)

    return (
        [texts]
        if isinstance(texts, Text)
        else texts
    )


def _determine_type_of(event):
    if "Records" in event:
        record = event["Records"][0]

        for key in _EVENT_SOURCE_KEYS:
            source = record.get(key)

            if source is not None:
                return EventType.from_string(
                    source[4:]
                )

    return EventType.CUSTOM


def _text_from_sns(event):
    message = event["Records"][0]["Sns"]
    attributes = message["MessageAttributes"]

    return Text(
        body=message["Message"],
        from_language=_language_attribute_value("from_language", attributes),
        to_language=_language_attribute_value("to_language", attributes)
    )


def _language_attribute_value(name, attributes):
    attribute = attributes.get(name, {})

    return _create_language(attribute.get("Value"))


def _create_language(name):
    return (Language.from_string(name)
            if name is not None
            else None)


def _text_from_sqs(event):
    return [
        _single_text_from_sqs(record)
        for record in event["Records"]
    ]


def _single_text_from_sqs(record):
    attributes = record["messageAttributes"]

    return Text(
        body=record["body"],
        from_language=_language_attribute_value("from_language", attributes),
        to_language=_language_attribute_value("to_language", attributes)
    )


def _text_from_custom_event(event):
    return Text(
        body=event.get("text", ""),
        from_language=_create_language(event.get("from_language")),
        to_language=_create_language(event.get("to_language"))
    )


def _text_from_kinesis(event):
    return [
        _single_text_from_kinesis(record)
        for record in event["Records"]
    ]


def _single_text_from_kinesis(record):
    return _text_from_custom_event(
        _decode_kinesis_data(record["kinesis"]["data"])
    )


def _decode_kinesis_data(d):
    str_data = base64.b64decode(d).decode("utf-8").strip()

    if str_data.startswith("{") and str_data.endswith("}"):
        try:
            return ast.literal_eval(str_data)
        except Exception:
            pass

    return {"text": str_data}
