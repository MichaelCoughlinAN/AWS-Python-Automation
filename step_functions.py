import boto3
import json
import logging
from botocore.exceptions import NoCredentialsError, ClientError

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()

def get_state_machine_arn(sfn_client, state_machine_name):
    try:
        # List all state machines and find the one with the matching name
        response = sfn_client.list_state_machines()
        for sm in response['stateMachines']:
            if sm['name'] == state_machine_name:
                return sm['stateMachineArn']
        return None
    except ClientError as e:
        logger.error(f"Error retrieving state machine ARN: {e}")
        raise

def manage_step_function(state_machine_name, action, role_arn, definition, region='us-west-1'):
    try:
        # Initialize the Step Functions client
        sfn_client = boto3.client('stepfunctions', region_name=region)

        if action in ['update', 'delete']:
            state_machine_arn = get_state_machine_arn(sfn_client, state_machine_name)
            if not state_machine_arn:
                return f"State machine '{state_machine_name}' not found."

        if action == 'create':
            # Create a new state machine
            response = sfn_client.create_state_machine(
                name=state_machine_name,
                definition=json.dumps(definition),
                roleArn=role_arn
            )
            logger.info(f"State machine {state_machine_name} created. Response: {response}")
            return f"State machine {state_machine_name} created."

        elif action == 'update':
            # Update an existing state machine
            response = sfn_client.update_state_machine(
                stateMachineArn=state_machine_arn,
                definition=json.dumps(definition),
                roleArn=role_arn
            )
            logger.info(f"State machine {state_machine_name} updated. Response: {response}")
            return f"State machine {state_machine_name} updated."

        elif action == 'delete':
            # Delete a state machine
            response = sfn_client.delete_state_machine(
                stateMachineArn=state_machine_arn
            )
            logger.info(f"State machine {state_machine_name} deleted. Response: {response}")
            return f"State machine {state_machine_name} deleted."

        else:
            logger.error("Invalid action specified")
            return "Invalid action specified. Please use 'create', 'update', or 'delete'."

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
    state_machine_name = 'STATE_MACHINE_NAME'  # Replace with your state machine name
    action = 'create'  # Replace with 'create', 'update', or 'delete'
    role_arn = 'ROLE_ARN'  # Replace with the ARN of the IAM role
    definition = {
        "Comment": "A simple AWS Step Functions state machine that automates a task.",
        "StartAt": "FirstState",
        "States": {
            "FirstState": {
                "Type": "Task",
                "Resource": "arn:aws:lambda:region:account-id:function:function-name",
                "End": True
            }
        }
    }  # Replace with your state machine definition
    region = 'REGION'  # Replace with your AWS region

    result = manage_step_function(state_machine_name, action, role_arn, definition, region)
    print(result)

if __name__ == "__main__":
    main()
