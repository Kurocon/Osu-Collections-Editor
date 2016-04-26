import struct
import logging

# Define byte lengths for different data types
OSU_BYTE = 1
OSU_SHORT = 2
OSU_INT = 4
OSU_LONG = 8
OSU_SINGLE = 4
OSU_DOUBLE = 8
OSU_BOOLEAN = 1
OSU_DATETIME = 8


def parse_string(fileobj):
    """
    Get an OSU string from the file object
    :param fileobj: The file object
    :type fileobj: FileIO[bytes]
    :return: The string
    """
    log = logging.getLogger(__name__)

    # Get next byte, this one indicates what the rest of the string is
    indicator = fileobj.read(1)

    if ord(indicator) == 0:
        # The next two parts are not present.
        # log.log(5, "Read empty STRING")
        return ""
    elif ord(indicator) == 11:
        # The next two parts are present.
        # The first part is a ULEB128. Get that.
        uleb = parse_uleb128(fileobj)
        # log.log(5, "Read {} as ULEB128".format(uleb))
        s = fileobj.read(uleb).decode('utf-8')
        # log.log(5, "Read {} as STRING".format(s))
        return s
    else:
        log.debug("Could not read valid STRING from the .db file. Probably something is going wrong in parsing.")
        return


def parse_uleb128(fileobj):
    """
    Get an Unsigned Little Endian Base 128 integer from the file object
    :param fileobj: The file object
    :type fileobj: FileIO[bytes]
    :return: The integer
    """

    result = 0
    shift = 0
    while True:
        byte = fileobj.read(1)[0]
        result |= (byte & 0x7F) << shift

        if ((byte & 0x80) >> 7) == 0:
            break

        shift += 7

    return result


def print_as_bits(byte):
    return "{0:b}".format(byte)


def get_int(integer):
    return struct.pack("I", integer)


def get_string(string):
    if not string:
        # If the string is empty, the string consists of just this byte
        return bytes([0x00])
    else:
        # Else, it starts with 0x0b
        result = bytes([0x0b])

        # Followed by the length of the string as an ULEB128
        result += get_uleb128(len(string))

        # Followed by the string in UTF-8
        result += string.encode('utf-8')
        return result


def get_uleb128(integer):
    cont_loop = True
    result = b''

    while cont_loop:
        byte = integer & 0x7F
        integer >>= 7
        if integer != 0:
            byte |= 0x80
        result += bytes([byte])
        cont_loop = integer != 0

    return result


def read_type(type, fobj):
    log = logging.getLogger(__name__)

    try:

        if type == "Int":
            bs = fobj.read(OSU_INT)
            # log.log(5, "Read {} as INT".format(bs))
            return int.from_bytes(bs, byteorder='little')
        elif type == "String":
            s = parse_string(fobj)
            return s
        elif type == "Byte":
            bs = fobj.read(OSU_BYTE)
            # log.log(5, "Read {} as BYTE".format(bs))
            return bs
        elif type == "Short":
            bs = fobj.read(OSU_SHORT)
            # log.log(5, "Read {} as SHORT".format(bs))
            return int.from_bytes(bs, byteorder='little')
        elif type == "Long":
            bs = fobj.read(OSU_LONG)
            # log.log(5, "Read {} as LONG".format(bs))
            return int.from_bytes(bs, byteorder='little')
        elif type == "Single":  # Also known as float
            bs = fobj.read(OSU_SINGLE)
            # log.log(5, "Read {} as SINGLE".format(bs))
            return struct.unpack('f', bs)
        elif type == "Double":
            bs = fobj.read(OSU_DOUBLE)
            # log.log(5, "Read {} as DOUBLE".format(bs))
            return struct.unpack('d', bs)
        elif type == "Boolean":
            bs = fobj.read(OSU_BOOLEAN)
            # log.log(5, "Read {} as BOOL".format(bs))
            return bs != b'\x00'
        elif type == "IntDoublepair":
            oxo8 = fobj.read(OSU_BYTE)
            # log.log(5, "Read {} as BYTE".format(oxo8))
            bs1 = fobj.read(OSU_INT)
            # log.log(5, "Read {} as INT".format(bs1))
            i = int.from_bytes(bs1, byteorder='little')
            oxob = fobj.read(OSU_BYTE)
            # log.log(5, "Read {} as BYTE".format(oxob))
            bs2 = fobj.read(OSU_DOUBLE)
            # log.log(5, "Read {} as DOUBLE".format(bs2))
            d = struct.unpack('d', bs2)
            return i, d
        elif type == "Timingpoint":
            bs1 = fobj.read(OSU_DOUBLE)
            # log.log(5, "Read {} as DOUBLE".format(bs1))
            bpm = struct.unpack('d', bs1)
            bs2 = fobj.read(OSU_DOUBLE)
            # log.log(5, "Read {} as DOUBLE".format(bs2))
            offset = struct.unpack('d', bs2)
            bs3 = fobj.read(OSU_BOOLEAN)
            # log.log(5, "Read {} as BOOL".format(bs3))
            uninherited = bs3 != b'\x00'
            return bpm, offset, uninherited
        elif type == "DateTime":
            bs = fobj.read(OSU_DATETIME)
            # log.log(5, "Read {} as DATETIME".format(bs))
            return int.from_bytes(bs, byteorder='little')
        else:
            log.warn("Error while reading .db file. I don't know how to read {}".format(type))

    except struct.error as e:
        log.warn("Error while parsing .db file. {}".format(e))
        raise e
