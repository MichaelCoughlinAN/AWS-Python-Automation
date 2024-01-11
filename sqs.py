import boto3
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

sqs_client = boto3.client('sqs')

def send_sqs_message(queue_url, message_body):
    try:
        response = sqs_client.send_message(QueueUrl=queue_url, MessageBody=message_body)
        logger.info(f"Message sent to SQS queue {queue_url}")
        return response
    except Exception as e:
        logger.error(f"Error sending message to SQS: {e}")
        raise

def receive_sqs_messages(queue_url, max_number_of_messages=10, wait_time_seconds=10):
    try:
        response = sqs_client.receive_message(
            QueueUrl=queue_url,
            MaxNumberOfMessages=max_number_of_messages,
            WaitTimeSeconds=wait_time_seconds
        )

        messages = response.get('Messages', [])
        for message in messages:
            process_message(message)
            delete_sqs_message(queue_url, message['ReceiptHandle'])
    except Exception as e:
        logger.error(f"Error receiving messages from SQS: {e}")
        raise

def process_message(message):
    # Placeholder for message processing logic
    print(message['Body'])

def delete_sqs_message(queue_url, receipt_handle):
    try:
        sqs_client.delete_message(QueueUrl=queue_url, ReceiptHandle=receipt_handle)
        logger.info(f"Message deleted from SQS queue {queue_url}")
    except Exception as e:
        logger.error(f"Error deleting message from SQS: {e}")
        raise

# Example usage
if __name__ == "__main__":
    try:
        sqs_queue_url = 'your-queue-url'
        sqs_response = send_sqs_message(sqs_queue_url, 'Hello from SQS!')
        print(sqs_response)
        receive_sqs_messages(sqs_queue_url)
    except Exception as e:
        logger.error(f"Error: {e}")
