import enum

from translation.language import Language
from translation.text import Text


@enum.unique
class EventType(enum.Enum):
    SNS = enum.auto()
    SQS = enum.auto()
    CUSTOM = enum.auto()


def lambda_handler(event, translator):
    texts = _texts_from(event)
    translations = translator.translate_many(texts)

    return {
        t.body: tr if isinstance(tr, str) else None
        for t, tr in zip(texts, translations)
    }


def _texts_from(event):
    t = _determine_type_of(event)

    text_from = (
        _text_from_sns
        if t is EventType.SNS
        else _text_from_sqs
        if t is EventType.SQS
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
        if len(event["Records"]) == 1:
            return EventType.SNS
        else:
            return EventType.SQS
    else:
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
