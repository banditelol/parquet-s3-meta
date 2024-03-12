import random
from faker import Faker
import polars as pl


def generate_fake_data(n: int = 1000) -> pl.DataFrame:
    fake = Faker()
    data = [
        {
            "name": fake.name(),
            "age": random.randint(0, 100),
            "address": fake.address().replace("\n", " "),
            "email": fake.email(),
            "job": fake.job(),
        }
        for _ in range(n)
    ]
    return pl.DataFrame(data)


if __name__ == "__main__":
    df = generate_fake_data(100_000)
    df.write_csv(
        "data/input/data.csv",
    )
    df.write_parquet("data/input/data.parquet")
    df.write_parquet("data/input/data_row.parquet", row_group_size=100)
    df.write_parquet("data/input/data_gzip.parquet", compression="gzip")
    df.write_parquet("data/input/data_brotli.parquet", compression="brotli")
