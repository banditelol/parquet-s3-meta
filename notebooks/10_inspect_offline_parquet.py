with open("data/input/data.parquet", "rb") as file:
    file.seek(-8, 2)  # Move the file pointer to the last 8 bytes
    footer_length = file.read(4)  # Read the last 8 bytes

    footer_length_int = int.from_bytes(footer_length, byteorder="little")

    file.seek(-8 - footer_length_int, 2)
    footer_byte = file.read(footer_length_int)
    print(footer_byte)
