# Experiment with parquet

## Introduction

This project is an experiment with parquet, a columnar storage file format. It explores its capabilities of reading metadata without loading the whole file and push down operation to optimize scanning.

## Prerequisite

You need the following prerequisite:
- create `.env` from `.env.example` and fill it as necessary
- create data folders `mkdir -p data/input -p data/minio`
- run `poetry install` to install the project
- run `docker compose up` to start `minio` a S3 compatible storage


## Experiments

1. generate fake data `poetry run python notebooks/00_fake_data.py`
2. prepare minio bucket and files `poetry run python notebooks/01_setup_minio.py`
3. try to load data partially to inspect only the metadata (ongoing) `poetry run python notebooks/10_inspect_offline_parquet_.py`
4. Use polars to compare lazy laoding (scan) with whole download `poetry run python notebooks/11_polars_lazy.py`

## TODO

- [ ] Continue experiment with reading metadata from byte data, may need to learn about Thrift Compact Protocol
- [ ] Find out how to monitor network call on minio to get the differences between using scan and load
- [ ] Try wireshark or MITM to get the traffic size based on hostname
- [ ] Create viz and accompanying article about the learnings

## Contributing

Contributions are welcome! If you find any issues or have suggestions for improvements, please open an issue or submit a pull request.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Contact

- Email: adityarputra@gmail.com
- Twitter: [@banditelolRP](https://twitter.com/banditelolRP)

## References

- `parquet-python` [a pure python implementation of parquet format](https://github.com/jcrobak/parquet-python/blob/master/parquet/encoding.py)
