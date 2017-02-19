###################################################################################################

variable "schedule_expression" {
  default = "cron(0 0 * * ? *)"
}

###################################################################################################

resource "aws_cloudwatch_event_rule" "trigger_requeue" {
  name                = "Trigger-Requeue-Lambda-${var.queue_name}"
  description         = "Scheduled execution of Requeue Lambda function"
  schedule_expression = "${var.schedule_expression}"
}

resource "aws_cloudwatch_event_target" "requeue_lambda" {
  rule      = "${aws_cloudwatch_event_rule.trigger_requeue.name}"
  arn       = "${aws_lambda_function.requeue.arn}"
  target_id = "RequeueLambda"
}

###################################################################################################
