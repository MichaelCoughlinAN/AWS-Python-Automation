import boto3
import logging
import os

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def upload_file_to_s3(bucket_name, file_name, object_name=None):
    """
    Upload a file to an S3 bucket.

    :param bucket_name: Name of the bucket to upload to.
    :param file_name: File to upload.
    :param object_name: S3 object name. If not specified, file_name is used.
    """
    try:
        if not os.path.isfile(file_name):
            logger.error(f"File not found: {file_name}")
            return

        s3_client = boto3.client('s3')
        if object_name is None:
            object_name = file_name

        s3_client.upload_file(file_name, bucket_name, object_name)
        logger.info(f"File {file_name} uploaded to {bucket_name}/{object_name}")
    except Exception as e:
        logger.error(f"Upload failed: {e}")
        raise

def download_file_from_s3(bucket_name, object_name, file_name):
    """
    Download a file from an S3 bucket.

    :param bucket_name: Bucket to download from.
    :param object_name: S3 object name.
    :param file_name: File to save the download.
    """
    try:
        s3_client = boto3.client('s3')
        s3_client.download_file(bucket_name, object_name, file_name)
        logger.info(f"File {object_name} downloaded from {bucket_name}")
    except Exception as e:
        logger.error(f"Download failed: {e}")
        raise

# Example usage
if __name__ == "__main__":
    try:
        # S3 example usage
        upload_file_to_s3('your-bucket-name', 'path/to/local/file')
        download_file_from_s3('your-bucket-name', 'object-key', 'path/to/save/file')
    except Exception as e:
        logger.error(f"Error: {e}")
