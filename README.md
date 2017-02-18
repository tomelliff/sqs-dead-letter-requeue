# SQS Dead Letter Requeue

Python Lambda function for handling SQS Dead Letter Queues.

Heavily inspired by [@Jimdo](https://github.com/Jimdo)'s Golang implementation of [SQS Dead Letter Handling](https://github.com/Jimdo/sqs-dead-letter-handling)

## Requirements

* Python 2.7

## Building it

### Just build the Lambda zip
```sh
make build
```

### Create an S3 bucket to store the Lambda function
```sh
make create_deploy_bucket
```

### Shipping the packaged Lambda function
```sh
make ship
```

### Deploy Lambda function plus scheduled event
Use the CloudFormation template provided (`cloudformation/requeue_lambda.yaml`)

## Running it locally

### Local setup/configuration

Make sure you have AWS credentials configured and a default region specified.

This can be with environment variables:

```sh
export AWS_ACCESS_KEY_ID=<my-access-key>
export AWS_SECRET_ACCESS_KEY=<my-secret-key>
export AWS_DEFAULT_REGION=<my-default-region>
```

or setting them in either an AWS credentials file (~/.aws/credentials) or AWS config file (~/.aws/config):

```
[default]
aws_access_key_id = <my-access-key>
aws_secret_access_key = <my-secret-key>
region = <my-default-region>
```

You will also need to set the name of the main queue to be requeued:

```sh
export QUEUE_NAME=<my-queue-name>
```

### Virtualenv/dependencies
```sh
virtualenv env
. env/bin/activate
pip install -r requirements.txt
```

### Run it
```sh
python requeue.py
```

## Generating test data

There is an included script to generate 100 messages on to a chosen queue. Run it:

```sh
python seed_queue.py ${QUEUE_NAME}_dead_letter
```
