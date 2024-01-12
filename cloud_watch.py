import boto3
import logging
from botocore.exceptions import NoCredentialsError, ClientError

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()

def create_cloudwatch_alarm(alarm_name, instance_id, namespace, metric_name, statistic, period, evaluation_periods, threshold, alarm_actions, region='us-west-1'):
    try:
        # Initialize the CloudWatch client
        cloudwatch_client = boto3.client('cloudwatch', region_name=region)

        # Create a CloudWatch alarm
        response = cloudwatch_client.put_metric_alarm(
            AlarmName=alarm_name,
            ComparisonOperator='GreaterThanThreshold',
            EvaluationPeriods=evaluation_periods,
            MetricName=metric_name,
            Namespace=namespace,
            Period=period,
            Statistic=statistic,
            Threshold=threshold,
            ActionsEnabled=True,
            AlarmActions=alarm_actions,
            AlarmDescription=f'Alarm when {metric_name} exceeds {threshold}',
            Dimensions=[
                {
                    'Name': 'InstanceId',
                    'Value': instance_id
                },
            ],
        )
        logger.info(f"CloudWatch alarm {alarm_name} created. Response: {response}")
        return f"CloudWatch alarm {alarm_name} created."

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
    alarm_name = 'ALARM_NAME'  # Replace with your alarm name
    instance_id = 'INSTANCE_ID'  # Replace with your EC2 instance ID
    namespace = 'AWS/EC2'  # Replace with the appropriate namespace
    metric_name = 'CPUUtilization'  # Replace with the metric of interest
    statistic = 'Average'  # Replace with 'Average', 'Sum', etc.
    period = 300  # Replace with the period in seconds
    evaluation_periods = 2  # Replace with the number of evaluation periods
    threshold = 70.0  # Replace with the threshold value
    alarm_actions = ['arn:aws:sns:region:account-id:alarm-topic']  # Replace with the ARN of the action to take
    region = 'REGION'  # Replace with your AWS region

    result = create_cloudwatch_alarm(alarm_name, instance_id, namespace, metric_name, statistic, period, evaluation_periods, threshold, alarm_actions, region)
    print(result)

if __name__ == "__main__":
    main()
