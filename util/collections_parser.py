import logging
import struct

from util.osu_parser import Difficulty2


class Collections:
    """
    :type version: int
    :type collections: list[Collection]
    """
    def __init__(self):
        self.version = 0
        self.collections = []

    def set_collection(self, name, collection):
        try:
            c = [c for c in self.collections if c.name == name][0]
        except KeyError:
            c = None

        if c is not None:
            i = self.collections.index(c)
            self.collections[i] = collection
        else:
            self.collections.append(collection)

    def get_collection(self, name):
        try:
            c = [c for c in self.collections if c.name == name][0]
        except KeyError:
            c = None

        return c


class Collection:
    """
    :type name: str
    :type beatmaps: list[CollectionMap]
    :type mapsets: list[util.osu_parser.Song]
    :type unmatched: list[CollectionMap]
    """
    def __init__(self):
        self.name = ""
        self.beatmaps = []
        self.mapsets = []
        self.unmatched = []

    def get_unmatched_song(self, song_hash):
        """
        Returns CollectionMap of the given unmatched hash
        :param song_hash:
        :return:
        """
        for s in self.unmatched:
            if s.hash == song_hash:
                return s
        return None

    def find_collectionmap_by_difficulty(self, difficulty_or_hash):
        """
        Finds the collectionmap object beloning to the given difficulty
        :param difficulty_or_hash: The difficulty or hash to search for
        :type difficulty_or_hash: Difficulty2|str
        :return: The collectionmap if found, else None
        :rtype: CollectionMap|None
        """
        if isinstance(difficulty_or_hash, str):
            for m in self.beatmaps:
                if m.hash == difficulty_or_hash:
                    return m
            else:
                return None
        elif isinstance(difficulty_or_hash, Difficulty2):
            for m in self.beatmaps:
                if m.difficulty == difficulty_or_hash:
                    return m
            else:
                return None
        else:
            return None

    def remove_song(self, song_difficulty_or_hash):
        found = None
        for m in self.beatmaps:
            if isinstance(song_difficulty_or_hash, str):
                if m.hash == song_difficulty_or_hash:
                    found = m
                    break
            elif isinstance(song_difficulty_or_hash, Difficulty2):
                if m.difficulty == song_difficulty_or_hash or m.hash == song_difficulty_or_hash.hash:
                    found = m
                    break

        if found:
            # Remove the map from the beatmap list
            self.beatmaps.remove(found)

            # We also need to remove the map from the mapset it belongs to
            for m in self.mapsets:
                if found.difficulty.hash in [d.hash for d in m.difficulties]:
                    # If the found difficulty is the same, remove it directly
                    if found.difficulty in m.difficulties:
                        m.difficulties.remove(found.difficulty)
                    # Else, find the entry in the list by hash, then remove it.
                    else:
                        for d in m.difficulties:
                            if d.hash == found.difficulty.hash:
                                m.difficulties.remove(d)
                                break

                    # If there are no maps in this mapset any more, remove it
                    if not m.difficulties:
                        self.mapsets.remove(m)
            return True
        else:
            # The song was not found in this collections' beatmaps. Try to remove it from the mapsets if it is in there.
            if isinstance(song_difficulty_or_hash, Difficulty2):
                for m in self.mapsets:
                    if song_difficulty_or_hash.hash in [d.hash for d in m.difficulties]:
                        for d in m.difficulties:
                            if d.hash == song_difficulty_or_hash.hash:
                                m.difficulties.remove(d)
                                break

                        # If there are no maps in this mapset any more, remove it
                        if not m.difficulties:
                            self.mapsets.remove(m)

            return False


class CollectionMap:
    """
    :type hash: str
    :type difficulty: util.osu_parser.Difficulty2
    :type mapset: util.osu_parser.Song
    :type from_api: bool
    """
    def __init__(self):
        self.hash = ""
        self.difficulty = None
        self.mapset = None
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
        log.debug("{} maps".format(collection_beatmap_count))

        # Then, for each beatmap in the collection:
        for j in range(0, collection_beatmap_count):
            # The MD5 hash for the song
            cm = CollectionMap()
            cm.hash = parse_string(fobj)
            c.beatmaps.append(cm)

        colls.collections.append(c)

    return colls


def parse_collections_gui(path, dialog):
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
    log.debug("There are {} collections in this DB".format(collection_count))

    collections_done = 0

    # Then, for each collection:
    for i in range(0, collection_count):
        dialog.progress.emit(int((collections_done/collection_count)*100))
        c = Collection()
        log.debug("Parsing collection {}".format(i))

        # The first part of the collection is the name of it.
        collection_name = parse_string(fobj)
        c.name = collection_name
        log.debug("Collection: {}".format(collection_name))
        dialog.current.emit(collection_name)

        # Then there is the number of beatmaps in the collection
        collection_beatmap_count = int.from_bytes(fobj.read(OSU_INT), byteorder='little')
        log.debug("{} maps".format(collection_beatmap_count))

        # Then, for each beatmap in the collection:
        for j in range(0, collection_beatmap_count):
            # The MD5 hash for the song
            cm = CollectionMap()
            cm.hash = parse_string(fobj)
            c.beatmaps.append(cm)

        colls.collections.append(c)
        collections_done += 1

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


##
# Save functions
##

# collection.db format
# Data type     Description
# Int           Version (e.g. 20150203)
# Int           Number of collections
#
# The following will be repeated for the total number of collections.
# String        Name of the collection
# Int           Number of beatmaps in the collection
# String*       Beatmap MD5 hash. Repeated for as many beatmaps as are in the collection.

def save_collection(collection, location):
    """
    Save the given collection database to the given location
    :param collection: The collection to save
    :type collection: Collections
    :param location: The file path to save the collection to
    :type location: str
    """

    # Open the output file
    log = logging.getLogger(__name__)
    log.debug("Saving CollectionDB to {}".format(location))
    log.debug("Opening file {}".format(location))
    fobj = open("{}".format(location), 'wb')

    # First write the collection version integer
    fobj.write(get_int(collection.version))

    # Then write the number of collections
    fobj.write(get_int(len(collection.collections)))

    # Then, for each collection
    for col in collection.collections:

        log.debug("Writing collection {}".format(col.name))

        # Write the collection name
        fobj.write(get_string(col.name))

        # Write the number of beatmaps in this collection
        fobj.write(get_int(len(col.beatmaps)))

        # Then for all beatmaps in the collection, write the MD5 hashes.
        for m in col.beatmaps:
            fobj.write(get_string(m.hash))

    # Close the file
    fobj.close()

    log.debug("Done saving collections.")


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
