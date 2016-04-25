import logging
import struct

from util.osudb_format import get_int, get_string, get_uleb128, parse_string, parse_uleb128, print_as_bits
from util.osudb_format import OSU_BOOLEAN, OSU_BYTE, OSU_DOUBLE, OSU_INT, OSU_LONG, OSU_SHORT, OSU_SINGLE
from util.oce_models import Collections, Collection, CollectionMap, Difficulty2


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
