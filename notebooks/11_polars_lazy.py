import polars as pl
from dotenv import load_dotenv
import os

load_dotenv()

if __name__ == "__main__":
    storage_options = {
        "endpoint_url": os.getenv("AWS_ENDPOINT_URL"),
        "access_key_id": os.getenv("AWS_ACCESS_KEY_ID"),
        "secret_access_key": os.getenv("AWS_SECRET_ACCESS_KEY"),
    }
    print(storage_options)
    # df = pl.read_csv("s3://data/test.csv", storage_options=storage_options)
    # print(df)
    # df = pl.read_csv("s3://data/data.csv", storage_options=storage_options)
    # print(df)
    # df = pl.scan_parquet("s3://data/data.parquet", storage_options=storage_options)
    # print(df.schema)
    for i in range(100):
        df = pl.read_parquet("s3://data/data.parquet", storage_options=storage_options)
    print(df)
