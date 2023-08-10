import base64

from translation import handler as hr
from translation import Language


class TestEventType:
    def test_from_valid_name(self):
        assert hr.EventType.from_string("sns") is hr.EventType.SNS

    def test_from_invalid_name_returns_custom(self):
        assert hr.EventType.from_string("invalid") is hr.EventType.CUSTOM


class TestCreateLanguage:
    def test_none_is_returned_for_none(self):
        assert hr._create_language(None) is None

    def test_language_instance_is_returned_for_name(self):
        assert hr._create_language("en") is Language.EN
        assert hr._create_language("pl") is Language.OTHER


class TestLanguageAttributeValue:
    def test_none_is_returned_for_missing_attribute(self):
        assert hr._language_attribute_value("lang", {}) is None

    def test_language_is_returned_when_present(self):
        lang = hr._language_attribute_value(
            "from_language",
            {"from_language": {"Value": "DE"}}
        )

        assert lang is Language.DE


class TestDetermineTypeOf:
    def test_for_sns(self, sns_event):
        assert hr._determine_type_of(sns_event) is hr.EventType.SNS

    def test_for_sqs(self, sqs_event):
        assert hr._determine_type_of(sqs_event) is hr.EventType.SQS

    def test_for_custom(self, custom_event):
        assert hr._determine_type_of(custom_event) is hr.EventType.CUSTOM

    def test_from_messed_up_custom_event(self, messed_up_custom_event):
        assert hr._determine_type_of(messed_up_custom_event) is hr.EventType.CUSTOM

    def test_for_kinesis(self, kinesis_event):
        assert hr._determine_type_of(kinesis_event) is hr.EventType.KINESIS


class TestTextRetrieval:
    def test_for_sns(self, sns_event, sns_text):
        assert hr._text_from_sns(sns_event) == sns_text

    def test_for_sqs(self, sqs_event, sqs_text):
        assert hr._text_from_sqs(sqs_event) == sqs_text

    def test_for_custom(self, custom_event, custom_event_text):
        assert hr._text_from_custom_event(custom_event) == custom_event_text

    def test_texts_from_for_sns(self, sns_event, sns_text):
        assert hr._texts_from(sns_event) == [sns_text]

    def test_texts_from_for_sqs(self, sqs_event, sqs_text):
        assert hr._texts_from(sqs_event) == sqs_text

    def test_texts_from_for_custom(self, custom_event, custom_event_text):
        assert hr._texts_from(custom_event) == [custom_event_text]

    def test_texts_from_for_kinesis(self, kinesis_event, kinesis_text):
        assert hr._texts_from(kinesis_event) == kinesis_text


class TestLambdaHandler:
    def test_for_sns(self, sns_event, sns_translation, translator):
        assert hr.lambda_handler(sns_event, translator) == sns_translation

    def test_for_sqs(self, sqs_event, sqs_translation, translator):
        assert hr.lambda_handler(sqs_event, translator) == sqs_translation

    def test_for_custom(self, custom_event, custom_event_translation, translator):
        assert hr.lambda_handler(custom_event, translator) == custom_event_translation

    def test_for_kinesis(self, kinesis_event, kinesis_translation, translator):
        assert hr.lambda_handler(kinesis_event, translator) == kinesis_translation


class TestDecodeKinesisData:
    def test_from_plain_string(self):
        original_data = "The cat is big"
        encoded_data = base64.b64encode(original_data.encode("utf-8"))

        assert hr._decode_kinesis_data(
            encoded_data
        ) == {"text": original_data}

    def test_from_dictionary(self):
        original_data = {"text": "Hello there", "to_language": "DE"}
        encoded_data = base64.b64encode(
            str(original_data).encode("utf-8")
        )

        assert hr._decode_kinesis_data(
            encoded_data
        ) == original_data
