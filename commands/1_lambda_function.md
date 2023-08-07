## Build the image
```bash
$ docker build -t poli-translator:vN .
```

## Run the image locally
```bash
# Start a container
$ docker run --name poli-translator -p 9000:8080 poli-translator:vN

# Run the handler with some event
$ curl "http://localhost:9000/2015-03-31/functions/function/invocations" -d '{"text": "sth"}'

# Terminate the container
$ docker container stop poli-translator
$ docker container rm poli-translator
```

## Log into docker with AWS ECR credentials

```bash
$ aws ecr get-login-password --region <REGION> --profile <PROFILE> | docker login --username AWS --password-stdin <ACCOUNT ID>.dkr.ecr.<REGION>.amazonaws.com
```

## Create a repository for the images on ECR (once only)

```bash
$ aws ecr create-repository --repository-name poli-translator --image-scanning-configuration scanOnPush=true --image-tag-mutability MUTABLE --profile <PROFILE>
```

## Tag and push the image

```bash
$ docker tag poli-translator:vN <REPO>/poli-translator:latest
$ docker push <REPO>/poli-translator:latest
```

## Create role and retrieve its ARN

```bash
# Set up the role if it doesn't exist
$ aws iam create-role --role-name lambda-ex --assume-role-policy-document '{"Version": "2012-10-17","Statement": [{ "Effect": "Allow", "Principal": {"Service": "lambda.amazonaws.com"}, "Action": "sts:AssumeRole"}]}' --profile <PROFILE>

# Attach policy to the newly created role
$ aws iam attach-role-policy --role-name lambda-ex --policy-arn arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole --profile <PROFILE>

# Retrieve the role's ARN
$ aws iam get-role --role-name lambda-ex --query 'Role.[RoleName, Arn]' --profile <PROFILE>
```


## Create function and invoke it
```bash
# Create the Lambda function if it doesn't exist
$ aws lambda create-function \
    --function-name poli-translator \
    --package-type Image \
    --code ImageUri=<URI> \
    --role <LAMBDA ROLE ARN> \
    --profile <RPOFILE>

# Invoke the function
$ aws lambda invoke --function-name poli-translator --payload '{"text": "sth"}' --cli-binary-format raw-in-base64-out --profile <PROFILE> response.json
```

## Updating the function

To update the function code we must:  

* rebuild the image

* test it locally

* log into Docker with AWS credentials

* tag and push the image

* use the update-function-code command to deploy the image to the Lambda function

  ```bash
  $ aws lambda update-function-code --function-name poli-translator --image-uri <URI> --profile <PROFILE> [--publish]
  ```

  Use the publish flag to publish a new function version.  
  
* invoke the function
