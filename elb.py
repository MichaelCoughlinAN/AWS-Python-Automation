import boto3
import logging
from botocore.exceptions import NoCredentialsError, ClientError

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()

def create_elb(load_balancer_name, subnets, security_groups, scheme='internet-facing', region='us-west-1'):
    try:
        # Initialize the ELB client
        elb_client = boto3.client('elbv2', region_name=region)

        # Create the load balancer
        response = elb_client.create_load_balancer(
            Name=load_balancer_name,
            Subnets=subnets,
            SecurityGroups=security_groups,
            Scheme=scheme,
            Type='application',
            IpAddressType='ipv4'
        )
        
        load_balancer_arn = response['LoadBalancers'][0]['LoadBalancerArn']
        logger.info(f"Load balancer {load_balancer_name} created with ARN: {load_balancer_arn}")
        return f"Load balancer {load_balancer_name} created successfully."

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
    load_balancer_name = 'LOAD_BALANCER_NAME'  # Replace with your load balancer name
    subnets = ['subnet-xxxxxxxx', 'subnet-yyyyyyyy']  # Replace with your subnet IDs
    security_groups = ['sg-xxxxxxxx']  # Replace with your security group IDs
    scheme = 'internet-facing'  # Replace with 'internet-facing' or 'internal'
    region = 'REGION'  # Replace with your AWS region

    result = create_elb(load_balancer_name, subnets, security_groups, scheme, region)
    print(result)

if __name__ == "__main__":
    main()
