import boto3

def send_sqs_message(queue_url, message_body):
    sqs_client = boto3.client('sqs')
    response = sqs_client.send_message(QueueUrl=queue_url, MessageBody=message_body)
    return response

def receive_sqs_messages(queue_url, max_number_of_messages=10, wait_time_seconds=10):
    sqs_client = boto3.client('sqs')
    response = sqs_client.receive_message(
        QueueUrl=queue_url,
        MaxNumberOfMessages=max_number_of_messages,
        WaitTimeSeconds=wait_time_seconds
    )

    messages = response.get('Messages', [])
    for message in messages:
        print(message['Body'])
        sqs_client.delete_message(
            QueueUrl=queue_url,
            ReceiptHandle=message['ReceiptHandle']
        )

# Example usage
if __name__ == "__main__":
    sqs_queue_url = 'your-queue-url'

    # Send a message to an SQS queue
    sqs_response = send_sqs_message(sqs_queue_url, 'Hello from SQS!')
    print(sqs_response)

    # Receive messages from an SQS queue
    receive_sqs_messages(sqs_queue_url)