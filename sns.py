import boto3

def publish_sns_message(topic_arn, message, subject):
    sns_client = boto3.client('sns')
    response = sns_client.publish(TopicArn=topic_arn, Message=message, Subject=subject)
    return response

# Example usage
if __name__ == "__main__":
    sns_topic_arn = 'arn:aws:sns:region:account-id:topic-name'

    # Publish a message to an SNS topic
    sns_response = publish_sns_message(sns_topic_arn, 'Hello from SNS!', 'SNS Subject')
    print(sns_response)
