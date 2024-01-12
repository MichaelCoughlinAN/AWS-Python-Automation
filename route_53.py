import boto3
import logging
from botocore.exceptions import NoCredentialsError, ClientError

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()

def manage_route53_record(hosted_zone_id, record_name, record_type, record_value, ttl, action, region='us-west-1'):
    try:
        # Initialize the Route 53 client
        route53_client = boto3.client('route53', region_name=region)

        change_batch = {
            'Changes': [
                {
                    'Action': action,
                    'ResourceRecordSet': {
                        'Name': record_name,
                        'Type': record_type,
                        'TTL': ttl,
                        'ResourceRecords': [{'Value': record_value}]
                    }
                }
            ]
        }

        if action in ['CREATE', 'UPSERT', 'DELETE']:
            # Modify the DNS record
            response = route53_client.change_resource_record_sets(
                HostedZoneId=hosted_zone_id,
                ChangeBatch=change_batch
            )
            logger.info(f"Route 53 record {record_name} {action.lower()}ed. Response: {response}")
            return f"Route 53 record {record_name} {action.lower()}ed successfully."
        else:
            logger.error("Invalid action specified")
            return "Invalid action specified. Please use 'CREATE', 'UPSERT', or 'DELETE'."

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
    hosted_zone_id = 'HOSTED_ZONE_ID'  # Replace with your hosted zone ID
    record_name = 'RECORD_NAME'  # Replace with the record name (e.g., 'example.com')
    record_type = 'RECORD_TYPE'  # Replace with the record type (e.g., 'A', 'CNAME')
    record_value = 'RECORD_VALUE'  # Replace with the record value (e.g., IP address for 'A' record)
    ttl = 300  # Replace with the TTL in seconds
    action = 'CREATE'  # Replace with 'CREATE', 'UPSERT', or 'DELETE'
    region = 'REGION'  # Replace with your AWS region

    result = manage_route53_record(hosted_zone_id, record_name, record_type, record_value, ttl, action, region)
    print(result)

if __name__ == "__main__":
    main()
