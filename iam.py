import boto3
import logging
from botocore.exceptions import NoCredentialsError, ClientError

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()

def manage_iam_role(role_name, action, policy_arn, description='IAM role description', region='us-east-1'):
    try:
        # Initialize the IAM client
        iam_client = boto3.client('iam', region_name=region)

        if action == 'create':
            # Create a new IAM role
            response = iam_client.create_role(
                RoleName=role_name,
                AssumeRolePolicyDocument='''{
                    "Version": "2012-10-17",
                    "Statement": [
                        {
                            "Effect": "Allow",
                            "Principal": {
                                "Service": "ec2.amazonaws.com"
                            },
                            "Action": "sts:AssumeRole"
                        }
                    ]
                }''',
                Description=description
            )
            # Attaching policy to the role
            iam_client.attach_role_policy(RoleName=role_name, PolicyArn=policy_arn)
            logger.info(f"IAM role {role_name} created. Response: {response}")
            return f"IAM role {role_name} created."

        elif action == 'update':
            # Update the description of an existing IAM role
            response = iam_client.update_role_description(
                RoleName=role_name,
                Description=description
            )
            logger.info(f"IAM role {role_name} updated. Response: {response}")
            return f"IAM role {role_name} updated."

        elif action == 'delete':
            # Detach policy before deleting the role
            iam_client.detach_role_policy(RoleName=role_name, PolicyArn=policy_arn)
            # Delete an IAM role
            response = iam_client.delete_role(RoleName=role_name)
            logger.info(f"IAM role {role_name} deleted. Response: {response}")
            return f"IAM role {role_name} deleted."

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
    role_name = 'ROLE_NAME'  # Replace with your IAM role name
    action = 'create'  # Replace with 'create', 'update', or 'delete'
    policy_arn = 'POLICY_ARN'  # Replace with your policy ARN
    description = 'DESCRIPTION'  # Replace with your role description
    region = 'REGION'  # Replace with your AWS region

    result = manage_iam_role(role_name, action, policy_arn, description, region)
    print(result)

if __name__ == "__main__":
    main()
