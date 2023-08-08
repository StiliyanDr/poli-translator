## Attach SQS permissions policy

```bash
$ aws iam attach-role-policy --role-name lambda-ex --policy-arn arn:aws:iam::aws:policy/service-role/AWSLambdaSQSQueueExecutionRole --profile <PROFILE>
```

## Create SQS queue

```bash
$ aws sqs create-queue --queue-name sqs-queue --profile <PROFILE>
```

## Create event-source-mapping

```bash
$ aws lambda create-event-source-mapping --function-name poli-translator --batch-size 10 --event-source-arn <queue ARN> --profile <PROFILE>
```

## Send a message to the queue

```bash
$ aws sqs send-message --queue-url <URL> --message-body "Hallo zusammen" --profile <PROFILE> [--message-attributes <ATTRS>]
```





