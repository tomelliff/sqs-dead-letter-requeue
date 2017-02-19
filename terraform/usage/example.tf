###################################################################################################

module "requeue" {
  source                       = "github.com/tomelliff/sqs-dead-letter-requeue//terraform/modules/requeue_lambda"
  queue_name                   = "queue_name"
  lambda_function_package_path = "../../requeue_lambda.zip"
}

###################################################################################################

