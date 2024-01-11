import boto3
import psycopg2

# Function to write data to a DynamoDB table
def write_to_dynamodb(table_name, data):
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table(table_name)
    table.put_item(Item=data)

# Function to read data from a DynamoDB table
def read_from_dynamodb(table_name, key):
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table(table_name)
    response = table.get_item(Key=key)
    return response.get('Item')

# Example usage
if __name__ == "__main__":
    # DynamoDB example usage
    write_to_dynamodb('your-dynamodb-table', {'PrimaryKey': 'value', 'attribute': 'data'})
    item = read_from_dynamodb('your-dynamodb-table', {'PrimaryKey': 'value'})
    print(item)
