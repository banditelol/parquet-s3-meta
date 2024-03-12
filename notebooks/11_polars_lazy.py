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

    print("Read Full Parquet")
    df = pl.read_parquet("s3://data/data.parquet", storage_options=storage_options)
    print(df.select(["email", "job"]))

    print("Scan Parquet")
    df = pl.scan_parquet(
        "s3://data/data_partial.parquet", storage_options=storage_options
    )
    print(df.select(["email", "job"]).collect())
    print(df.head(5).collect())

    print("Row Parquet")
    df = pl.scan_parquet("s3://data/data_row.parquet", storage_options=storage_options)
    print(df.select(["email", "job"]).collect())
    print(df.head(5).collect())

    print("Row GZIP")
    df = pl.scan_parquet("s3://data/data_gzip.parquet", storage_options=storage_options)
    print(df.select(["email", "job"]).collect())
    print(df.head(5).collect())

    print("Row Brotli")
    df = pl.scan_parquet(
        "s3://data/data_brotli.parquet", storage_options=storage_options
    )
    print(df.select(["email", "job"]).collect())
    print(df.head(5).collect())
