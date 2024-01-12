import boto3
import logging
from botocore.exceptions import NoCredentialsError, ClientError

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()

def manage_ec2_instance(instance_id, action, region='us-west-1'):
    try:
        # Initialize the EC2 client
        ec2_client = boto3.client('ec2', region_name=region)

        if action == 'start':
            # Start the EC2 instance
            response = ec2_client.start_instances(InstanceIds=[instance_id])
            logger.info(f"Start request for instance {instance_id} sent. Response: {response}")
            return f"Instance {instance_id} is starting."
        
        elif action == 'stop':
            # Stop the EC2 instance
            response = ec2_client.stop_instances(InstanceIds=[instance_id])
            logger.info(f"Stop request for instance {instance_id} sent. Response: {response}")
            return f"Instance {instance_id} is stopping."
        
        else:
            logger.error("Invalid action specified")
            return "Invalid action specified. Please use 'start' or 'stop'."

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
    instance_id = 'INSTANCE_ID'  # Replace with your instance ID
    action = 'start'  # Replace with 'start' or 'stop'
    region = 'REGION'  # Replace with your AWS region

    result = manage_ec2_instance(instance_id, action, region)
    print(result)

if __name__ == "__main__":
    main()
