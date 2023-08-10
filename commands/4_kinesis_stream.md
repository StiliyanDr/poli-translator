## Attach Kinesis stream read permissions to the execution role

```bash
$ aws iam attach-role-policy --role-name lambda-ex --policy-arn arn:aws:iam::aws:policy/service-role/AWSLambdaKinesisExecutionRole --profile <PROFILE>
```

## Create a Kinesis stream

```bash
$ aws kinesis create-stream --stream-name lambda-stream --shard-count 1 --profile <PROFILE>
$ aws kinesis describe-stream --stream-name lambda-stream --profile <PROFILE>
```

## Create an event-source-mapping for the stream in Lambda

```bash
$ aws lambda create-event-source-mapping --function-name poli-translator --event-source  <stream arn> --batch-size 100 --starting-position LATEST --profile <PROFILE>
$ aws lambda list-event-source-mappings --function-name poli-translator --profile <PROFILE>
```

## Add a record to the stream

```bash
$ aws kinesis put-record --stream-name lambda-stream --partition-key 1 --data $(echo -n 'Hallo zusammen' | base64) --profile <PROFILE>
```

