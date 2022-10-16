import boto3
import botocore
import logging

def main():
    unique_prefix = 'thisisatest'
    region = 'us-west-2'
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)
    s3_bucket = f'{unique_prefix}-discord-event-handler-source'
    generate_lambda_source(s3_bucket,region)

def generate_lambda_source(s3_bucket,region):
    try:
        if region is None:
            s3_client = boto3.client('s3')
            s3_client.create_bucket(
                Bucket=s3_bucket,
                ACL='private')
            s3_client.upload_file("../src/discord_event_handler.zip", s3_bucket, "discord_event_handler.zip")
        else:
            s3_client = boto3.client('s3', region_name=region)
            location = {'LocationConstraint': region}
            s3_client.create_bucket(
                Bucket=s3_bucket,
                CreateBucketConfiguration=location,
                ACL='private')
    except botocore.exceptions.ClientError as e:
        logging.error(e)
        return False
    return True


if __name__ == "__main__":
    main()
 