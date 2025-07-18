provider "aws" {
    region = var.AWS_REGION
    secret_key = var.AWS_SECRET_ACCESS_KEY
    access_key = var.AWS_ACCESS_KEY_ID
}

## S3 Bucket

resource "aws_s3_bucket" "long-term-storage-s3-bucket" {
    bucket = "c17-narcus-plant-bucket"
    force_destroy = true
}

## ECR Repositories

resource "aws_ecr_repository" "alerts-lambda-ecr-repository" {
  name = "c17-narcus-alerts-lambda"
  image_tag_mutability = "MUTABLE"
  image_scanning_configuration {
    scan_on_push = true
  }
  force_delete = true
}

resource "aws_ecr_repository" "historical-data-ecr-repository" {
  name = "c17-narcus-historical-sensor-readings-ecr"
  image_tag_mutability = "MUTABLE"
  image_scanning_configuration {
    scan_on_push = true
  }
  force_delete = true
}

resource "aws_ecr_repository" "short-term-data-ecr-repository" {
  name = "c17-narcus-lmnh-botany"
  image_tag_mutability = "MUTABLE"
  image_scanning_configuration {
    scan_on_push = true
  }
  force_delete = true
}


data "aws_ecr_repository" "lambda-image-repo" {
  name = "c17-narcus-lmnh-botany"
}

data "aws_ecr_image" "lambda-image-version" {
  repository_name = data.aws_ecr_repository.lambda-image-repo.name
  image_tag       = "latest"
}

# Trust doc
data "aws_iam_policy_document" "lambda-role-trust-policy-doc" {
    statement {
      effect = "Allow"
      principals {
        type = "Service"
        identifiers = [ "lambda.amazonaws.com" ]
      }
      actions = [
        "sts:AssumeRole"
      ]
    }
}

# Permissions doc
data "aws_iam_policy_document" "lambda-role-permissions-policy-doc" {
    statement {
      effect = "Allow"
      actions = [
        "logs:CreateLogGroup",
        "logs:CreateLogStream",
        "logs:PutLogEvents"
      ]
      resources = [ "arn:aws:logs:eu-west-2:129033205317:*" ]
    }
}

# Role
resource "aws_iam_role" "lambda-role" {
    name = "c17-narcus-pipeline-lambda-terraform-role"
    assume_role_policy = data.aws_iam_policy_document.lambda-role-trust-policy-doc.json
}

# Permissions policy
resource "aws_iam_policy" "lambda-role-permissions-policy" {
    name = "c17-narcus-pipeline-lambda-permissions-policy"
    policy = data.aws_iam_policy_document.lambda-role-permissions-policy-doc.json
}

# Connect the policy to the role
resource "aws_iam_role_policy_attachment" "lambda-role-policy-connection" {
  role = aws_iam_role.lambda-role.name
  policy_arn = aws_iam_policy.lambda-role-permissions-policy.arn
}

## Lambda

resource "aws_lambda_function" "simple-email-lambda" {
  function_name = "c17-narcus-pipeline-lambda-tf"
  role = aws_iam_role.lambda-role.arn
  package_type = "Image"
  image_uri = data.aws_ecr_image.lambda-image-version.image_uri
  timeout = 60
  environment {
    variables = {
        DB_HOST = var.DB_HOST
        DB_PORT = var.DB_PORT
        DB_USER = var.DB_USER
        DB_PASSWORD = var.DB_PASSWORD
        DB_NAME = var.DB_NAME
        DB_SCHEMA = var.DB_SCHEMA
        DB_DRIVER = var.DB_DRIVER
    }
  }
}