import struct


def _get_footer_size(file_obj):
    """Read the footer size in bytes, which is serialized as little endian."""
    file_obj.seek(-8, 2)  # Move the file pointer to the last 8 bytes
    tup = struct.unpack(b"<i", file_obj.read(4))
    return tup[0]


def _get_footer(file_obj, footer_length_int):
    file_obj.seek(-8 - footer_length_int, 2)
    return file_obj.read(footer_length_int)


def _get_version(footer_bytes):
    tup = struct.unpack(b"<i", footer_bytes[:4])
    return tup[0]


if __name__ == "__main__":
    with open("data/input/data.parquet", "rb") as file:
        footer_length = _get_footer_size(file)
        print(f"Footer Length: {footer_length} bytes")
        # Footer Length: 909 bytes

        footer_byte = _get_footer(file, footer_length)
        print("Footer Bytes:")
        print(footer_byte)
        # b'\x15\x04\x19lH\x04root...\x1c\x00\x00\x00'

        version_int = _get_version(footer_byte)
        print(f"\nVersion Int:{version_int}")
        # Version Int: 1813578773
