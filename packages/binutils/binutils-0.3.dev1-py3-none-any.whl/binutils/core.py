def int_to_little_endian_bytes(integer):
    """Converts a two-bytes integer into a pair of one-byte integers using
    the little-endian notation (i.e. the less significant byte first).

    The `integer` input must be a 2 bytes integer, i.e. `integer` must be
    greater or equal to 0 and less or equal to 65535 (0xffff in hexadecimal
    notation).

    For instance, with the input decimal value ``integer=700`` (0x02bc in
    hexadecimal notation) this function will return the tuple ``(0xbc, 0x02)``.

    :param int integer: the 2 bytes integer to be converted. It must be in
        range (0, 0xffff).
    """

    # Check argument type to make exception messages more explicit
    if not isinstance(integer, int):
        msg = "An integer in range(0x00, 0xffff) is required (got {})."
        raise TypeError(msg.format(type(integer)))

    # Check the argument value
    if not (0 <= integer <= 0xffff):
        msg = "An integer in range(0x00, 0xffff) is required (got {})."
        raise ValueError(msg.format(integer))

    hex_string = '%04x' % integer
    hex_tuple = (int(hex_string[2:4], 16), int(hex_string[0:2], 16))

    return hex_tuple


def little_endian_bytes_to_int(little_endian_byte_seq):
    """Converts a pair of bytes into an integer.

    The `little_endian_byte_seq` input must be a 2 bytes sequence defined
    according to the little-endian notation (i.e. the less significant byte
    first).

    For instance, if the `little_endian_byte_seq` input is equals to
    ``(0xbc, 0x02)`` this function returns the decimal value ``700`` (0x02bc in
    hexadecimal notation).

    :param bytes little_endian_byte_seq: the 2 bytes sequence to be converted.
        It must be compatible with the "bytes" type and defined according to the
        little-endian notation.
    """

    # Check the argument and convert it to "bytes" if necessary.
    # Assert "little_endian_byte_seq" items are in range (0, 0xff).
    # "TypeError" and "ValueError" are sent by the "bytes" constructor if
    # necessary.
    # The statement "tuple(little_endian_byte_seq)" implicitely rejects
    # integers (and all non-iterable objects) to compensate the fact that the
    # bytes constructor doesn't reject them: bytes(2) is valid and returns
    # b'\x00\x00'
    little_endian_byte_seq = bytes(tuple(little_endian_byte_seq))

    # Check that the argument is a sequence of two items
    if len(little_endian_byte_seq) != 2:
        raise ValueError("A sequence of two bytes is required.")

    integer = little_endian_byte_seq[1] * 0x100 + little_endian_byte_seq[0]

    return integer


def pretty_hex_str(byte_seq, separator=","):
    """Converts a squence of bytes to a string of hexadecimal numbers.

    For instance, with the input tuple ``(255, 0, 10)``
    this function will return the string ``"ff,00,0a"``.

    :param bytes byte_seq: a sequence of bytes to process. It must be
        compatible with the "bytes" type.
    :param str separator: the string to be used to separate each byte in the
        returned string (default ",").
    """

    # Check the argument and convert it to "bytes" if necessary.
    # This conversion assert "byte_seq" items are in range (0, 0xff).
    # "TypeError" and "ValueError" are sent by the "bytes" constructor if
    # necessary.
    if isinstance(byte_seq, int):
        byte_seq = bytes((byte_seq, ))
    else:
        byte_seq = bytes(byte_seq)

    return separator.join(['%02x' % byte for byte in byte_seq])


def int_to_bits(n: int) -> list:
    # https://stackoverflow.com/a/10322018
    #return [n >> i & 1 for i in range(n.bit_length() - 1,-1,-1)]
    return [1 if digit=='1' else 0 for digit in bin(n)[2:]]


def int_to_bits_str(n: int) -> str:
    bit_list = int_to_bits(n)
    return "".join([str(bit) for bit in bit_list])


def bits_to_int(bit_list: list) -> int:
    # https://stackoverflow.com/a/12461400
    out = 0
    for bit in bit_list:
        out = (out << 1) | bit
    return out


def swap_bytes(bit_list: list) -> list:
    pass

def swap_bits_in_bytes(bit_list: list) -> list:
    pass

def set_lsb_to_zero(n):
    """Pour fixer le LSB à 0 : Utilisez l'opération AND (&) avec le complément de 1 (c'est-à-dire ~1)."""
    return n & ~1

def set_lsb_to_one(n):
    """Pour fixer le LSB à 1 : Utilisez l'opération OR (|) avec 1."""
    return n | 1

def toggle_lsb(n):
    """Pour permuter la valeur du bit de poids le plus faible (LSB pour "least significant bit") d'une variable entière en Python, vous pouvez utiliser l'opération XOR (^) avec la valeur 1. Ceci va changer le LSB de 0 à 1 ou de 1 à 0, selon sa valeur initiale."""
    return n ^ 1

def is_lsb_one(n):
    return (n & 1) == 1

def extract_integer_from_bits(bits: str, start: int, end: int) -> int:
    """
    Extracts an integer from a string of bits.

    Args:
        bits (str): A string of bits, e.g. '10101010'.
        start (int): The starting index of the bits to extract.
        end (int): The ending index of the bits to extract.

    Returns:
        int: The integer value of the extracted bits.

    Raises:
        ValueError: If the start or end index is out of range, or if the
            extracted bits do not represent a valid integer.
    """
    return int(bits[start:end], 2)