import pyarrow.parquet as pq

metadata = pq.read_metadata("data/input/data.parquet")
...
