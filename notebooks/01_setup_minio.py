import boto3
from dotenv import load_dotenv
import os

if __name__ == "__main__":
    load_dotenv()

    s3_client = boto3.client(
        "s3",
        endpoint_url=os.getenv("AWS_ENDPOINT_URL"),
        aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
        aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
        aws_session_token=None,
        config=boto3.session.Config(signature_version="s3v4"),
        verify=False,
    )

    s3_client.delete_object(Bucket="data", Key="data.csv")
    s3_client.delete_object(Bucket="data", Key="data.parquet")
    s3_client.delete_bucket(Bucket="data")

    s3_client.create_bucket(Bucket="data")
    s3_client.upload_file("data/input/data.csv", "data", "data.csv")
    s3_client.upload_file("data/input/data.parquet", "data", "data.parquet")
