## Create a topic

```bash
$ aws sns create-topic --name sns-topic-for-lambda --profile <PROFILE>
```

## Grant the topic permission to invoke the lambda function

```bash
$ aws lambda add-permission --function-name poli-translator --source-arn <SNS ARN> --statement-id function-with-sns --action "lambda:InvokeFunction" --principal sns.amazonaws.com --profile <PROFILE>
```

## Subscribe the lambda function to the topic

```bash
$ aws sns subscribe --protocol lambda --region <REGION> --topic-arn <SNS ARN> --notification-endpoint <lambda ARN> --profile <PROFILE>
```

## Publish a message to the topic to invoke the function

```bash
$ aws sns publish --message "Hallo zusammen!" --topic-arn <topic ARN> --profile <PROFILE>
```

