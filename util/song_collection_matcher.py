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

    # Construct dictionary of {"hash": ("beatmap", "mapset")}
    lookup_dict = {}
    for song in songs.songs:
        for diff in song.difficulties:
            lookup_dict[diff.hash] = (diff, song)

    matched_count = 0
    unmatched_count = 0
    unmatched_maps = []

    for collection in collections.collections:
        for diff in collection.beatmaps:
            try:
                diff.difficulty, diff.mapset = lookup_dict[diff.hash]
                if diff.mapset not in collection.mapsets:
                    collection.mapsets.append(diff.mapset)
                matched_count += 1
            except KeyError:
                collection.unmatched.append(diff)
                unmatched_maps.append(diff)
                unmatched_count += 1

        # Get a list of all diffs in all mapsets of this collection
        col_songs = []
        for mapset in collection.mapsets:
            for diff in mapset.difficulties:
                col_songs.append(diff)

        # Remove all of the difficulties actually present from the list of diffs
        for collmap in collection.beatmaps:
            if collmap.difficulty in col_songs:
                col_songs.remove(collmap.difficulty)

        # Remove all left over songs in the list from the mapsets in the collection
        for m in collection.mapsets:
            diffs = m.difficulties
            for d in diffs:
                if d in col_songs:
                    m.difficulties.remove(d)

    log.debug("Matching done. {} matched and {} unmatched.".format(matched_count, unmatched_count))

    return collections, matched_count, unmatched_count, unmatched_maps
