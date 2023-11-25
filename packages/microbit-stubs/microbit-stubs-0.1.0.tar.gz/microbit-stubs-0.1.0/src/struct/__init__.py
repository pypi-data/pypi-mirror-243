"""
Pack and unpack primitive data types
"""


def calcsize(fmt: str) -> int:
    """
    Get the number of bytes needed to store the given fmt.
    :param fmt: A format string.
    :return: The number of bytes needed to store such a value.
    """


def pack(fmt: str, v1, *vn) -> bytearray:
    """
    Pack values according to a format string.
    :param fmt: The format string.
    :param v1: The first value.
    :param vn: The remaining values.
    :return: A bytes object encoding the values.
    """


def pack_into(fmt: str, buffer: bytearray, offset: int, v1, *vn) -> None:
    """
    Pack values according to a format string.
    :param fmt: The format string.
    :param buffer: The target buffer to write into.
    :param offset: he offset into the buffer. May be negative to count from the end of the buffer.
    :param v1: The first value.
    :param vn: The remaining values.
    """


def unpack(fmt: str, data) -> tuple:
    """
    Unpack data according to a format string.
    :param fmt: The format string.
    :param data: The data.
    :return: A tuple of the unpacked values.
    """


def unpack_from(fmt: str, buffer: bytearray, offset: int = 0) -> tuple:
    """
    Unpack data from a buffer according to a format string.
    :param fmt: The format string.
    :param buffer: The source buffer to read from.
    :param offset: The offset into the buffer. May be negative to count from the end of the buffer.
    :return: A tuple of the unpacked values.
    """