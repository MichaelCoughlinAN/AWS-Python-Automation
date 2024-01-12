import boto3
import logging
from botocore.exceptions import NoCredentialsError, ClientError

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()

def manage_api_gateway(api_name, action, resource_name, http_method, lambda_function_arn, region='us-west-1'):
    try:
        # Initialize the API Gateway client
        api_gateway_client = boto3.client('apigateway', region_name=region)

        if action == 'create':
            # Create a new REST API
            api_response = api_gateway_client.create_rest_api(
                name=api_name,
                description='API created by script',
                endpointConfiguration={
                    'types': ['REGIONAL']
                }
            )
            api_id = api_response['id']
            logger.info(f"REST API {api_name} created with ID: {api_id}")

            # Get the root resource ID
            resources = api_gateway_client.get_resources(restApiId=api_id)
            root_id = [resource for resource in resources['items'] if resource['path'] == '/'][0]['id']

            # Create a new resource under the root resource
            resource_response = api_gateway_client.create_resource(
                restApiId=api_id,
                parentId=root_id,
                pathPart=resource_name
            )
            resource_id = resource_response['id']
            logger.info(f"Resource {resource_name} created with ID: {resource_id}")

            # Create a new method on the resource
            method_response = api_gateway_client.put_method(
                restApiId=api_id,
                resourceId=resource_id,
                httpMethod=http_method,
                authorizationType='NONE'
            )
            logger.info(f"Method {http_method} created on resource {resource_name}")

            # Integrate the method with a Lambda function
            uri = f'arn:aws:apigateway:{region}:lambda:path/2015-03-31/functions/{lambda_function_arn}/invocations'
            integration_response = api_gateway_client.put_integration(
                restApiId=api_id,
                resourceId=resource_id,
                httpMethod=http_method,
                type='AWS_PROXY',
                integrationHttpMethod='POST',
                uri=uri
            )
            logger.info(f"Integrated method {http_method} with Lambda function: {lambda_function_arn}")

            return f"API Gateway {api_name} created successfully."

        elif action == 'delete':
            # Delete an existing REST API (APIs are identified by their API ID, not name)
            api_id = 'your-api-id'  # Replace with your API ID
            api_gateway_client.delete_rest_api(restApiId=api_id)
            logger.info(f"REST API {api_name} deleted.")
            return f"API Gateway {api_name} deleted successfully."

        else:
            logger.error("Invalid action specified")
            return "Invalid action specified. Please use 'create' or 'delete'."

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
    api_name = 'API_NAME'  # Replace with your API name
    action = 'create'  # Replace with 'create' or 'delete'
    resource_name = 'RESOURCE_NAME'  # Replace with your resource name
    http_method = 'HTTP_METHOD'  # Replace with your HTTP method (e.g., 'GET', 'POST')
    lambda_function_arn = 'LAMBDA_FUNCTION_ARN'  # Replace with your Lambda function ARN
    region = 'REGION'  # Replace with your AWS region

    result = manage_api_gateway(api_name, action, resource_name, http_method, lambda_function_arn, region)
    print(result)

if __name__ == "__main__":
    main()
