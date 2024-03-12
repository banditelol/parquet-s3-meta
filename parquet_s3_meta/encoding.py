"""encoding.py - methods for reading parquet encoded data blocks."""

from __future__ import absolute_import, division, print_function, unicode_literals
import json
import logging
import os
import struct

import thriftpy2 as thriftpy
from thriftpy2.protocol.compact import TCompactProtocolFactory
from thriftpy2.transport import TTransportBase


class TFileTransport(TTransportBase):  # pylint: disable=too-few-public-methods
    """TTransportBase implementation for decoding data from a file object."""

    def __init__(self, fo):
        """Initialize with `fo`, the file object to read from."""
        self._fo = fo
        self._pos = fo.tell()

    def _read(self, sz):
        """Read data `sz` bytes."""
        return self._fo.read(sz)

    def open(self):
        """Open which is a no-op."""
        if not self.is_open():
            raise ValueError("Already closed.")

    def is_open(self):
        """Return true if open."""
        return not self._fo.closed

    def close(self):
        """Close the file object."""
        self._fo.close()

    def read(self, sz):
        """Read data `sz` bytes."""
        return self._fo.read(sz)

    def write(self, buf):
        """Write buf to the file object."""
        self._fo.write(buf)

    def flush(self):
        """Flush the output."""
        self._fo.flush()


THRIFT_FILE = os.path.join(os.path.dirname(__file__), "parquet.thrift")
parquet_thrift = thriftpy.load(THRIFT_FILE, module_name=str("parquet_thrift"))  # pylint: disable=invalid-name

logger = logging.getLogger("parquet")  # pylint: disable=invalid-name


def _get_footer_size(last_8_bytes):
    """Read the footer size in bytes, which is serialized as little endian."""
    tup = struct.unpack(b"<i", last_8_bytes[:4])
    return tup[0]


def _read_footer(file_obj):
    """Read the footer from the given file object and returns a FileMetaData object.

    This method assumes that the fo references a valid parquet file.
    """
    file_obj.seek(-8, 2)
    last_8_bytes = file_obj.read(8)
    footer_size = _get_footer_size(last_8_bytes)
    if logger.isEnabledFor(logging.DEBUG):
        logger.debug("Footer size in bytes: %s", footer_size)
    file_obj.seek(-(8 + footer_size), 2)  # seek to beginning of footer
    tin = TFileTransport(file_obj)
    pin = TCompactProtocolFactory().get_protocol(tin)
    fmd = parquet_thrift.FileMetaData()
    fmd.read(pin)
    return fmd


def _parse_footer(fmd):
    row_group_col = fmd.row_groups[0].columns[0].__dict__
    row_group_col["meta_data"] = row_group_col["meta_data"].__dict__
    schema = fmd.schema[1].__dict__
    footer = {
        "version": fmd.version,
        "schema": schema,
        "row_group_col": row_group_col,
    }
    return footer


if __name__ == "__main__":
    with open("data/input/data.parquet", "rb") as file:
        fmd = _read_footer(file)
        footer = _parse_footer(fmd)
        print(json.dumps(footer, indent=2))
