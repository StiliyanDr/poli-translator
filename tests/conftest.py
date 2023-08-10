import base64

import pytest

import translation as tr


@pytest.fixture
def translator():
    return tr.Translator()


@pytest.fixture
def english_text():
    return "hello young sir"


@pytest.fixture
def unsupported_language_text():
    return "witaj młody panie"


@pytest.fixture
def german_text():
    return "Hallo junger Herr"


@pytest.fixture
def french_text():
    return "bonjour jeune monsieur"


@pytest.fixture
def sns_event():
    return {"Records": [
        {
            "EventVersion": "1.0",
            "EventSubscriptionArn": "arn",
            "EventSource": "aws:sns",
            "Sns": {
                "SignatureVersion": "1",
                "Timestamp": "2019-01-02T12:45:07.000Z",
                "Signature": "tcc6faL2yUC6dgZdmrwh1Y4c",
                "SigningCertUrl": "url",
                "MessageId": "95df01b4-9903-4c2231d41eb5e",
                "Message": "Hello, I am SNS",
                "MessageAttributes": {
                    "from_language": {
                        "Type": "String",
                        "Value": "EN"
                    },
                    "to_language": {
                        "Type": "String",
                        "Value": "FR"
                    }
                },
                "Type": "Notification",
                "UnsubscribeUrl": "url",
                "TopicArn": "arn",
                "Subject": "TestInvoke",
            }
        }
    ]}


@pytest.fixture
def sns_text(sns_event):
    return tr.Text(
        body=sns_event["Records"][0]["Sns"]["Message"],
        from_language=tr.Language.from_string(
            sns_event["Records"][0]["Sns"]["MessageAttributes"][
                "from_language"
            ]["Value"]
        ),
        to_language=tr.Language.from_string(
            sns_event["Records"][0]["Sns"]["MessageAttributes"][
                "to_language"
            ]["Value"]
        )
    )


@pytest.fixture
def sns_translation(sns_text):
    return {sns_text.body: "Bonjour, je suis SNS"}


@pytest.fixture
def sqs_event():
    return {"Records": [
        {
            "body": "Hello, this is SQS 1",
            "messageAttributes": {
                "from_language": {
                    "Type": "String",
                    "Value": "EN"
                },
                "to_language": {
                    "Type": "String",
                    "Value": "FR"
                }
            },
            "messageId": "059f36b4-87a3-44ab-83d2-661975830a7d",
            "receiptHandle": "AQEBwJnKyrHigUMZj6rYigCgxlaS3SLy0a...",
            "attributes": {
                "ApproximateReceiveCount": "1",
                "SentTimestamp": "1545082649183",
                "SenderId": "AIDAIENQZJOLO23YVJ4VO",
                "ApproximateFirstReceiveTimestamp": "1545082649185"
            },
            "md5OfBody": "e4e68fb7bd0e697a0ae8f1bb342846b3",
            "eventSource": "aws:sqs",
            "eventSourceARN": "arn",
            "awsRegion": "us-east-2"
        },
        {
            "body": "Hello, this is SQS 2",
            "messageAttributes": {
                "from_language": {
                    "Type": "String",
                    "Value": "EN"
                },
                "to_language": {
                    "Type": "String",
                    "Value": "FR"
                }
            },
            "messageId": "2e1424d4-f796-459a-8184-9c92662be6da",
            "receiptHandle": "AQEBzWwaftRI0KuVm4tP+/7q1rGgNqicHq...",
            "attributes": {
                "ApproximateReceiveCount": "1",
                "SentTimestamp": "1545082650636",
                "SenderId": "AIDAIENQZJOLO23YVJ4VO",
                "ApproximateFirstReceiveTimestamp": "1545082650649"
            },
            "md5OfBody": "e4e68fb7bd0e697a0ae8f1bb342846b3",
            "eventSource": "aws:sqs",
            "eventSourceARN": "arn",
            "awsRegion": "us-east-2"
        }
    ]}


@pytest.fixture
def sqs_translation(sqs_text):
    return {
        sqs_text[0].body: "Bonjour, c'est SQS 1",
        sqs_text[1].body: "Bonjour, c'est SQS 2",
    }


@pytest.fixture
def sqs_text(sqs_event):
    return [
        tr.Text(
            body=sqs_event["Records"][0]["body"],
            from_language=tr.Language.from_string(
                sqs_event["Records"][0]["messageAttributes"][
                    "from_language"
                ]["Value"]
            ),
            to_language=tr.Language.from_string(
                sqs_event["Records"][0]["messageAttributes"][
                    "to_language"
                ]["Value"]
            )
        ),
        tr.Text(
            body=sqs_event["Records"][1]["body"],
            from_language=tr.Language.from_string(
                sqs_event["Records"][0]["messageAttributes"][
                    "from_language"
                ]["Value"]
            ),
            to_language=tr.Language.from_string(
                sqs_event["Records"][0]["messageAttributes"][
                    "to_language"
                ]["Value"]
            )
        ),
    ]


@pytest.fixture
def custom_event():
    return {
        "text": "Custom text",
        "from_language": "EN",
        "to_language": "DE"
    }


@pytest.fixture
def custom_event_text(custom_event):
    return tr.Text(
        body=custom_event["text"],
        from_language=tr.Language.from_string(
            custom_event["from_language"]
        ),
        to_language=tr.Language.from_string(
            custom_event["to_language"]
        )
    )


@pytest.fixture
def custom_event_translation(custom_event_text):
    return {
        custom_event_text.body: "Benutzerdefinierter Text"
    }


@pytest.fixture
def messed_up_custom_event():
    return {
        "Records": [
            {
                "key": "value"
            }
        ]
    }


@pytest.fixture
def kinesis_event():
    return {
        "Records": [
            {
                "kinesis": {
                    "kinesisSchemaVersion": "1.0",
                    "partitionKey": "1",
                    "sequenceNumber": "4959033827",
                    "data": base64.b64encode(str({
                        "text": "Hallo zusammen",
                        "from_language": "DE",
                        "to_language": "EN",
                    }).encode("utf-8")),
                    "approximateArrivalTimestamp": 1545084650.987
                },
                "eventSource": "aws:kinesis",
                "eventVersion": "1.0",
                "eventID": "shardId-000000000006:49590",
                "eventName": "aws:kinesis:record",
                "invokeIdentityArn": "arn",
                "awsRegion": "us-east-2",
                "eventSourceARN": "arn"
            },
            {
                "kinesis": {
                    "kinesisSchemaVersion": "1.0",
                    "partitionKey": "1",
                    "sequenceNumber": "4959033831",
                    "data": base64.b64encode(
                        "Le chat est grand".encode("utf-8")
                    ),
                    "approximateArrivalTimestamp": 1545084650.987
                },
                "eventSource": "aws:kinesis",
                "eventVersion": "1.0",
                "eventID": "shardId-000000000006:49590",
                "eventName": "aws:kinesis:record",
                "invokeIdentityArn": "arn",
                "awsRegion": "us-east-2",
                "eventSourceARN": "arn"
            }
        ]
    }


@pytest.fixture
def kinesis_text():
    return [
        tr.Text(
            body="Hallo zusammen",
            from_language=tr.Language.DE,
            to_language=tr.Language.EN
        ),
        tr.Text(
            body="Le chat est grand"
        ),
    ]


@pytest.fixture
def kinesis_translation(kinesis_text):
    return {
        kinesis_text[0].body: "Hello everyone",
        kinesis_text[1].body: "The cat is big",
    }
