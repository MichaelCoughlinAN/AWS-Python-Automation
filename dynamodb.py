import boto3
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def get_dynamodb_resource():
    """
    Create and return a DynamoDB resource.
    Ensure AWS credentials and region are configured in your environment.
    """
    try:
        dynamodb = boto3.resource('dynamodb')
        return dynamodb
    except Exception as e:
        logger.error(f"Error in getting DynamoDB resource: {e}")
        raise

def write_to_dynamodb(table_name, data):
    """
    Write data to a DynamoDB table.

    :param table_name: Name of the DynamoDB table.
    :param data: Data to be written (dictionary format).
    """
    try:
        dynamodb = get_dynamodb_resource()
        table = dynamodb.Table(table_name)
        table.put_item(Item=data)
        logger.info(f"Data written to table {table_name}: {data}")
    except Exception as e:
        logger.error(f"Error writing to DynamoDB: {e}")
        raise

def read_from_dynamodb(table_name, key):
    """
    Read data from a DynamoDB table.

    :param table_name: Name of the DynamoDB table.
    :param key: Key for the item to be read (dictionary format).
    :return: Item if found, None otherwise.
    """
    try:
        dynamodb = get_dynamodb_resource()
        table = dynamodb.Table(table_name)
        response = table.get_item(Key=key)
        item = response.get('Item')
        if item:
            logger.info(f"Item found in table {table_name}: {item}")
        else:
            logger.info(f"No item found with key {key} in table {table_name}")
        return item
    except Exception as e:
        logger.error(f"Error reading from DynamoDB: {e}")
        raise

# Example usage
if __name__ == "__main__":
    try:
        # DynamoDB example usage
        table_name = 'your-dynamodb-table'
        data_to_write = {'PrimaryKey': 'value', 'attribute': 'data'}
        key_to_read = {'PrimaryKey': 'value'}

        write_to_dynamodb(table_name, data_to_write)
        item = read_from_dynamodb(table_name, key_to_read)
        print(item)

    except Exception as e:
        logger.error(f"Error in DynamoDB operations: {e}")
