import boto3

# Function to upload a file to an S3 bucket
def upload_file_to_s3(bucket_name, file_name, object_name=None):
    s3_client = boto3.client('s3')
    if object_name is None:
        object_name = file_name
    s3_client.upload_file(file_name, bucket_name, object_name)

# Function to download a file from an S3 bucket
def download_file_from_s3(bucket_name, object_name, file_name):
    s3_client = boto3.client('s3')
    s3_client.download_file(bucket_name, object_name, file_name)

# Example usage
if __name__ == "__main__":
    # S3 example usage
    upload_file_to_s3('your-bucket-name', 'path/to/local/file')
    download_file_from_s3('your-bucket-name', 'object-key', 'path/to/save/file')
