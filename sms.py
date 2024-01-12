import boto3
from botocore.exceptions import NoCredentialsError, PartialCredentialsError, ParamValidationError

def send_sms(phone_number, message, region_name='your-aws-region'):
    try:
        # Initialize the SNS client
        sns_client = boto3.client('sns', region_name=region_name)

        # Send the SMS message
        response = sns_client.publish(
            PhoneNumber=phone_number,
            Message=message
        )

        return response['MessageId']

    except NoCredentialsError:
        return "AWS credentials are missing or invalid. Please configure your AWS credentials."
    except PartialCredentialsError:
        return "Incomplete AWS credentials. Please check your AWS credentials configuration."
    except ParamValidationError as e:
        return f"Parameter validation error: {str(e)}"
    except Exception as e:
        return f"An error occurred while sending the SMS: {str(e)}"

def main():
    phone_number = '+1234567890'  # Replace with the recipient's phone number
    message = 'Hello from AWS SNS!'
    region_name = 'your-aws-region'  # Replace with your AWS region

    result = send_sms(phone_number, message, region_name)

    if isinstance(result, str) and len(result) > 0:  # Check if result is a MessageId
        print(f"SMS sent with message ID: {result}")
    else:
        print(f"Error: {result}")

if __name__ == "__main__":
    main()
