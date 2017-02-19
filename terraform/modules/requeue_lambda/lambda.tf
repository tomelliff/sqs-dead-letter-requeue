###################################################################################################

variable "queue_name" {}
variable "lambda_function_package_path" {}

###################################################################################################

resource "aws_lambda_function" "requeue" {
  filename         = "${var.lambda_function_package_path}"
  function_name    = "Requeue-${var.queue_name}"
  description      = "Requeues messages from dead letter queue"
  runtime          = "python2.7"
  role             = "${aws_iam_role.lambda_role.arn}"
  handler          = "requeue.handler"
  source_code_hash = "${base64sha256(file("${var.lambda_function_package_path}"))}"
  timeout          = 60

  environment {
    variables = {
      QUEUE_NAME = "${var.queue_name}"
    }
  }
}

###################################################################################################
