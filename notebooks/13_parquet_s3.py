import json
import boto3
from dotenv import load_dotenv
import os
from io import BytesIO
from parquet_s3_meta.encoding import _get_footer_size, _read_footer, _parse_footer

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

    response = s3_client.head_object(Bucket="data", Key="data.parquet")
    content_length = response["ContentLength"]
    print(f"content_length : {content_length}")
    response = s3_client.get_object(
        Bucket="data",
        Key="data.parquet",
        Range=f"bytes={content_length-8}-{content_length}",
    )
    footer_size = _get_footer_size(response["Body"].read())
    print(f"footer_size: {footer_size}")
    response = s3_client.get_object(
        Bucket="data",
        Key="data.parquet",
        Range=f"bytes={content_length-8-footer_size}-{content_length}",
    )
    footer_file = BytesIO(response["Body"].read())
    print(json.dumps(_parse_footer(_read_footer(footer_file)), indent=2))
