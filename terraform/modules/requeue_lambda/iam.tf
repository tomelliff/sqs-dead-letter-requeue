###################################################################################################

resource "aws_iam_role" "lambda_role" {
  name = "Requeue-${var.queue_name}"

  assume_role_policy = <<EOF
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Action": "sts:AssumeRole",
      "Principal": {
        "Service": "lambda.amazonaws.com"
      },
      "Effect": "Allow",
      "Sid": ""
    }
  ]
}
EOF
}

resource "aws_iam_role_policy" "lambda_logging_policy" {
  role = "${aws_iam_role.lambda_role.id}"
  name = "logging"

  policy = <<EOF
{
  "Version"  : "2012-10-17",
  "Statement": [
    {
      "Sid"     : "1",
      "Effect"  : "Allow",
      "Action"  : [ "logs:CreateLogGroup",
                    "logs:PutLogEvents",
                    "logs:CreateLogStream",
                    "logs:DescribeLogStreams" ],
      "Resource": "arn:aws:logs:*:*:*"
    }
  ]
}
EOF
}

resource "aws_iam_role_policy" "lambda_sqs_policy" {
  role = "${aws_iam_role.lambda_role.id}"
  name = "sqs"

  policy = <<EOF
{
  "Version"  : "2012-10-17",
  "Statement": [
    {
      "Sid"     : "1",
      "Effect"  : "Allow",
      "Action"  : [ "sqs:ChangeMessageVisibilityBatch",
                    "sqs:DeleteMessage",
                    "sqs:DeleteMessageBatch",
                    "sqs:GetQueueAttributes",
                    "sqs:GetQueueUrl",
                    "sqs:ListQueues",
                    "sqs:ReceiveMessage",
                    "sqs:SendMessage",
                    "sqs:SendMessageBatch" ],
      "Resource": "arn:aws:sqs:*:*:${var.queue_name}*"
    }
  ]
}
EOF
}

###################################################################################################
