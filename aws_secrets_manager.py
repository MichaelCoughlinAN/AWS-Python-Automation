import boto3
import logging
from botocore.exceptions import NoCredentialsError, ClientError

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()

def manage_secret(secret_name, secret_value, action, region='us-west-1'):
    try:
        # Initialize the Secrets Manager client
        secrets_manager_client = boto3.client('secretsmanager', region_name=region)

        if action == 'create':
            # Create a new secret
            response = secrets_manager_client.create_secret(
                Name=secret_name,
                SecretString=secret_value
            )
            logger.info(f"Secret {secret_name} created. Response: {response}")
            return f"Secret {secret_name} created successfully."

        elif action == 'retrieve':
            # Retrieve an existing secret
            response = secrets_manager_client.get_secret_value(
                SecretId=secret_name
            )
            secret = response['SecretString']
            logger.info(f"Secret {secret_name} retrieved.")
            return f"Retrieved secret: {secret}"

        else:
            logger.error("Invalid action specified")
            return "Invalid action specified. Please use 'create' or 'retrieve'."

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
    secret_name = 'SECRET_NAME'  # Replace with your secret name
    secret_value = 'SECRET_VALUE'  # Replace with your secret value
    action = 'create'  # Replace with 'create' or 'retrieve'
    region = 'REGION'  # Replace with your AWS region

    result = manage_secret(secret_name, secret_value, action, region)
    print(result)

if __name__ == "__main__":
    main()
