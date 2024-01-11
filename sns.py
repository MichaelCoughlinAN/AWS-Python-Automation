import boto3
import logging
import os

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def publish_sns_message(topic_arn, message, subject):
    """
    Publish a message to an Amazon SNS topic.

    :param topic_arn: The ARN of the SNS topic.
    :param message: The message to publish.
    :param subject: The subject of the message.
    :return: The response from the SNS service.
    """
    try:
        sns_client = boto3.client('sns')
        response = sns_client.publish(TopicArn=topic_arn, Message=message, Subject=subject)
        logger.info("Message published to SNS topic.")
        return response
    except Exception as e:
        logger.error(f"Failed to publish message: {e}")
        raise

# Example usage
if __name__ == "__main__":
    try:
        sns_topic_arn = os.getenv('SNS_TOPIC_ARN', 'arn:aws:sns:region:account-id:topic-name')
        sns_response = publish_sns_message(sns_topic_arn, 'Hello from SNS!', 'SNS Subject')
        print(sns_response)
    except Exception as e:
        logger.error(f"Error: {e}")
