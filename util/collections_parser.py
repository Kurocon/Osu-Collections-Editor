import logging


class Collections:
    """
    :type collection_count: int
    :type version: int
    :type collections: list[Collection]
    """
    def __init__(self):
        self.collection_count = 0
        self.version = 0
        self.collections = []

    def get_collection(self, name):
        for collection in self.collections:
            if collection.name == name:
                return collection

        return None


class Collection:
    """
    :type name: str
    :type beatmap_count: int
    :type beatmaps: list[CollectionMap]
    """
    def __init__(self):
        self.name = ""
        self.beatmap_count = 0
        self.beatmaps = []


class CollectionMap:
    """
    :type hash: str
    :type difficulty: util.osu_parser.Difficulty2
    :type from_api: bool
    """
    def __init__(self):
        self.hash = ""
        self.difficulty = None
        self.from_api = False

# Define byte lengths for different data types
OSU_BYTE = 1
OSU_SHORT = 2
OSU_INT = 4
OSU_LONG = 8
OSU_SINGLE = 4
OSU_DOUBLE = 8
OSU_BOOLEAN = 1


# collection.db format
# Data type     Description
# Int           Version (e.g. 20150203)
# Int           Number of collections
#
# The following will be repeated for the total number of collections.
# String        Name of the collection
# Int           Number of beatmaps in the collection
# String*       Beatmap MD5 hash. Repeated for as many beatmaps as are in the collection.


def parse_collections(path):
    log = logging.getLogger(__name__)
    log.debug("Reading .osu file {}".format(path))
    log.debug("Opening file {}".format(path))
    fobj = open("{}".format(path), 'rb')

    colls = Collections()

    # Try to parse the file as a collection db.
    # First the version, which is an int
    version = int.from_bytes(fobj.read(OSU_INT), byteorder='little')
    colls.version = version
    log.debug("CollectionDB version {}".format(version))

    # Then the number of collections, also an int
    collection_count = int.from_bytes(fobj.read(OSU_INT), byteorder='little')
    colls.collection_count = collection_count
    log.debug("There are {} collections in this DB".format(collection_count))

    # Then, for each collection:
    for i in range(0, collection_count):
        c = Collection()
        log.debug("Parsing collection {}".format(i))

        # The first part of the collection is the name of it.
        collection_name = parse_string(fobj)
        c.name = collection_name
        log.debug("Collection: {}".format(collection_name))

        # Then there is the number of beatmaps in the collection
        collection_beatmap_count = int.from_bytes(fobj.read(OSU_INT), byteorder='little')
        c.beatmap_count = collection_beatmap_count
        log.debug("{} maps".format(collection_beatmap_count))

        # Then, for each beatmap in the collection:
        for j in range(0, collection_beatmap_count):
            # The MD5 hash for the song
            cm = CollectionMap()
            cm.hash = parse_string(fobj)
            c.beatmaps.append(cm)

        colls.collections.append(c)

    return colls


def parse_string(fileobj):
    """
    Get an OSU string from the file object
    :param fileobj: The file object
    :type fileobj: FileIO[bytes]
    :return: The string
    """

    # Get next byte, this one indicates what the rest of the string is
    indicator = fileobj.read(1)

    if ord(indicator) == 0:
        # The next two parts are not present.
        return ""
    elif ord(indicator) == 11:
        # The next two parts are present.
        # The first part is a ULEB128. Get that.
        uleb = parse_uleb128(fileobj)
        return fileobj.read(uleb).decode('utf-8')
    else:
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
