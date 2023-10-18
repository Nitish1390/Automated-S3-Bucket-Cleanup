import boto3
from datetime import datetime, timedelta

def delete_old_files(event, context):
    bucket_name = 'your_bucket_name'  # Replace with your S3 bucket name
    retention_days = 30

    s3 = boto3.client('s3')

    # Calculate the date 30 days ago from now
    deletion_date = datetime.now() - timedelta(days=retention_days)

    # List objects in the bucket
    objects = s3.list_objects_v2(Bucket=bucket_name)

    # Delete objects older than 30 days
    if 'Contents' in objects:
        for obj in objects['Contents']:
            last_modified = obj['LastModified']
            if last_modified.replace(tzinfo=None) < deletion_date:
                s3.delete_object(Bucket=bucket_name, Key=obj['Key'])
                print(f'Deleted object: {obj["Key"]}')
    else:
        print('No objects found in the bucket.')

    return {
        'statusCode': 200,
        'body': 'Files older than 30 days deleted successfully.'
    }

