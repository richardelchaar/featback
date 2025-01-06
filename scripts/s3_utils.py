import boto3
import botocore.exceptions
import pandas as pd
import json
from scripts.configuration import AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY



bucket_name = "featback1"


# Initialize S3 client
try:
    s3_client = boto3.client(
        's3',
        aws_access_key_id=AWS_ACCESS_KEY_ID,
        aws_secret_access_key=AWS_SECRET_ACCESS_KEY
    )
except botocore.exceptions.ClientError as e:
    raise RuntimeError(f"Error initializing S3 client: {e}")


def store_posts_in_data_lake(posts, product,subreddit):

    """Store raw reddit posts in JSON format to s3 bucket."""

    for post in posts:
        body = json.dumps(post).encode('utf-8')
        s3_client.put_object(
            Body=body,
            Bucket="featback1",
            Key=f"data/reddit_submissions/{subreddit}/{product}/{post['id']}.json"
        )

    print(f"Stored {len(posts)} posts in S3 bucket.")


def load_json_files_from_s3(prefix):
    """Load JSON files from an S3 bucket and return a concatenated DataFrame."""
    try:
        response = s3_client.list_objects_v2(Bucket=bucket_name, Prefix=prefix)
        if 'Contents' not in response:
            return pd.DataFrame()

        json_files = [obj['Key'] for obj in response.get('Contents', []) if obj['Key'].endswith('.json')]

        df_list = []
        for json_file in json_files:
            try:
                obj = s3_client.get_object(Bucket=bucket_name, Key=json_file)
                json_content = json.loads(obj['Body'].read().decode('utf-8'))
                df_list.append(pd.DataFrame([json_content]))
            except Exception as e:
                continue  # Skip the file if there's an issue

        return pd.concat(df_list, ignore_index=True) if df_list else pd.DataFrame()
    except botocore.exceptions.ClientError as e:
        raise RuntimeError(f"Error accessing S3 bucket: {e}")


def save_last_processed_timestamp_to_s3(timestamp, file_key):
    """Save the last processed post timestamp to S3."""
    try:
        s3_client.put_object(Body=str(timestamp), Bucket=bucket_name, Key=file_key)
    except Exception as e:
        raise RuntimeError(f"Error saving timestamp to S3: {e}")



def get_last_processed_timestamp_from_s3(file_key):
    try:
        obj = s3_client.get_object(Bucket=bucket_name, Key=file_key)
        return float(obj['Body'].read().decode('utf-8'))
    except botocore.exceptions.ClientError as e:
        return 0  # If no file exists, start from timestamp 0
