import logging


def match_songs_to_collections(songs, collections):
    """
    Match songs to collections
    :param songs: Songs object
    :type songs: Songs
    :param collections: Collections object
    :type collections: Collections
    :return: Tuple of matched collections, number matched, number unmatched, and a list of unmatched maps
    :rtype: tuple(Collections, int, int, list[CollectionMap])
    """

    log = logging.getLogger(__name__)
    log.debug("Matching {} songs and {} collections".format(len(songs.songs), collections.collection_count))

    # Construct dictionary of {"hash": "beatmap"}
    lookup_dict = {}
    for song in songs.songs:
        for diff in song.difficulties:
            lookup_dict[diff.hash] = diff

    matched_count = 0
    unmatched_count = 0
    unmatched_maps = []

    for collection in collections.collections:
        for diff in collection.beatmaps:
            try:
                diff.difficulty = lookup_dict[diff.hash]
                matched_count += 1
            except KeyError:
                unmatched_maps.append(diff)
                unmatched_count += 1

    log.debug("Matching done. {} matched and {} unmatched.".format(matched_count, unmatched_count))

    return collections, matched_count, unmatched_count, unmatched_maps
