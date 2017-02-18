SOURCES=requeue.py
TESTS=
CLOUDFORMATION_TEMPLATES=cloudformation/requeue_lambda.yaml
PACKAGE_NAME=requeue_lambda.zip
AWS_ACCOUNT_ID=$(shell aws sts get-caller-identity --output text --query Account)
DEPLOY_BUCKET_NAME=lambda-functions-$(AWS_DEFAULT_REGION)-$(AWS_ACCOUNT_ID)

$(PACKAGE_NAME): $(SOURCES)
	zip $(PACKAGE_NAME) $(SOURCES)

build: test_code $(PACKAGE_NAME)

test_code:
	python -m unittest discover

validate_cloudformation: $(CLOUDFORMATION_TEMPLATES)
	$(foreach CLOUDFORMATION_TEMPLATE,$(CLOUDFORMATION_TEMPLATES),aws cloudformation validate-template --template-body file://$(CLOUDFORMATION_TEMPLATE);)

test: test_code validate_cloudformation

create_deploy_bucket:
	region_constraints='--region $(AWS_DEFAULT_REGION) --create-bucket-configuration LocationConstraint=$(AWS_DEFAULT_REGION)'; \
	aws s3api create-bucket --bucket $(DEPLOY_BUCKET_NAME) $${region_constraints}

ship: build
	aws_account_id=`aws sts get-caller-identity --output text --query Account`; \
	aws s3 cp $(PACKAGE_NAME) s3://$(DEPLOY_BUCKET_NAME)
