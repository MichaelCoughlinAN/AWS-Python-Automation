import boto3
import logging
import re
import os
import time
from botocore.exceptions import NoCredentialsError, ClientError

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()

def is_valid_email(email):
    # Basic email format validation
    return re.match(r"[^@]+@[^@]+\.[^@]+", email)

def send_email_ses(sender, recipient, aws_region, subject, body_text, body_html):
    try:
        # Validate email addresses
        if not is_valid_email(sender) or not is_valid_email(recipient):
            raise ValueError("Invalid sender or recipient email format")

        # Initialize the SES client
        ses_client = boto3.client('ses', region_name=aws_region)

        # Send the email
        response = ses_client.send_email(
            Source=sender,
            Destination={'ToAddresses': [recipient]},
            Message={
                'Subject': {'Data': subject},
                'Body': {
                    'Text': {'Data': body_text},
                    'Html': {'Data': body_html}
                }
            }
        )
        logger.info(f"Email sent! Message ID: {response['MessageId']}")
        return f"Email sent! Message ID: {response['MessageId']}"

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
    sender = os.getenv('SENDER_EMAIL')  # Set this in your environment variables
    recipient = os.getenv('RECIPIENT_EMAIL')  # Set this in your environment variables
    if not sender or not recipient:
        logger.error("Sender or recipient email not set in environment variables.")
        return

    aws_region = 'AWS_REGION'  # Replace with your AWS region
    subject = 'SUBJECT'  # Replace with your email subject
    body_text = 'BODY_TEXT'  # Replace with your email body text
    body_html = '<html><body><h1>BODY_HTML</h1></body></html>'  # Replace with your email body HTML

    for attempt in range(3):  # Retry up to 3 times
        result = send_email_ses(sender, recipient, aws_region, subject, body_text, body_html)
        if "Message ID" in result:
            print(result)
            break
        else:
            logger.error(f"Attempt {attempt + 1} failed. Retrying...")
            time.sleep(2 ** attempt)  # Exponential backoff

if __name__ == "__main__":
    main()
