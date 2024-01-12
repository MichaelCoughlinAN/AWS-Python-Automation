import boto3
from botocore.exceptions import NoCredentialsError, ClientError
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()

def manage_lambda_function(function_name, action, region='us-west-1', s3_bucket='your-s3-bucket', zip_file='your-function.zip'):
    try:
        # Initialize the Lambda client
        lambda_client = boto3.client('lambda', region_name=region)

        if action == 'create':
            # Create a new Lambda function
            with open(zip_file, 'rb') as f:
                zip_content = f.read()
            response = lambda_client.create_function(
                FunctionName=function_name,
                Runtime='python3.8',
                Role='your-iam-role-arn',  # Replace with your IAM role ARN
                Handler='lambda_function.lambda_handler',  # Replace with your handler
                Code={'ZipFile': zip_content},
                Description='A sample Lambda function'
            )
            logger.info(f"Lambda function {function_name} created. Response: {response}")
            return f"Lambda function {function_name} created."

        elif action == 'update':
            # Update an existing Lambda function code
            with open(zip_file, 'rb') as f:
                zip_content = f.read()
            response = lambda_client.update_function_code(
                FunctionName=function_name,
                ZipFile=zip_content
            )
            logger.info(f"Lambda function {function_name} updated. Response: {response}")
            return f"Lambda function {function_name} updated."

        elif action == 'delete':
            # Delete a Lambda function
            response = lambda_client.delete_function(FunctionName=function_name)
            logger.info(f"Lambda function {function_name} deleted. Response: {response}")
            return f"Lambda function {function_name} deleted."

        else:
            logger.error("Invalid action specified")
            return "Invalid action specified. Please use 'create', 'update', or 'delete'."

    except NoCredentialsError:
        logger.error("No AWS credentials found")
        return "AWS credentials are missing or invalid. Please configure your AWS credentials."
    except ClientError as e:
        logger.error(f"AWS Client error: {e}")
        return f"AWS Client error: {str(e)}"
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        return f"An error occurred: {str(e)}"

def main():
    function_name = 'LAMBDA_FUNCTION_NAME'  # Replace with your Lambda function name
    action = 'create'  # Replace with 'create', 'update', or 'delete'
    region = 'REGION'  # Replace with your AWS region
    s3_bucket = 'S3_BUCKET'  # Replace with your S3 bucket name
    zip_file = 'ZIP_FILE'  # Replace with your zip file name

    result = manage_lambda_function(function_name, action, region, s3_bucket, zip_file)
    print(result)

if __name__ == "__main__":
    main()
