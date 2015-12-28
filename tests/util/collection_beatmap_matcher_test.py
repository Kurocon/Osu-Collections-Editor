import sys
from pprint import pprint

import util.osu_parser
import util.collections_parser

if __name__ == "__main__":

    default_collection_path = "/data/OwnCloud/Osu Program/collection.db"
    default_songs_path = "/data/OwnCloud/Osu Songs"

    print("------------------------------------------------------------------")
    print(" Osu Collection<->Beatmap matcher Test")
    print("------------------------------------------------------------------")
    print("Input the path to your OSU! collection.db, or enter to use the default.")
    print("The default is \"{}\"".format(default_collection_path))

    collection_path = input("Path: ")

    if not collection_path:
        collection_path = default_collection_path

    print("Input your OSU! music directory path, or enter to use the default.")
    print("The default is \"{}\"".format(default_songs_path))

    songs_path = input("Path: ")

    if not songs_path:
        songs_path = default_songs_path

    print("")
    print("Using {} as the collections path.".format(collection_path))
    print("Using {} as the songs path.".format(songs_path))
    print("------------------------------------------------------------------")
    print("")
    print("Loading collection database...")

    collections = util.collections_parser.parse_collections(collection_path)
    ccount = collections.collection_count
    scount = sum([i.beatmap_count for i in collections.collections])

    print("There are {} collection{} with a total of {} song{} in this database.".format(ccount, "" if ccount == 1 else "s", scount, "" if scount == 1 else "s"))
    print("")
    print("------------------------------------------------------------------")
    print("")
    print("Loading songs...")

    song_dirs = util.osu_parser.find_songs(songs_path)
    sorted_song_dirs = sorted(song_dirs)

    songs = util.osu_parser.Songs()

    for song_str in sorted_song_dirs:
        song = util.osu_parser.Song()
        difficulties = song_dirs.get(song_str)
        sorted_difficulties = sorted(difficulties)

        for difficulty_str in sorted_difficulties:
            try:
                difficulty = util.osu_parser.Difficulty2.from_file("/".join([songs_path, song_str, difficulty_str]), difficulty_str[:-4])
                song.add_difficulty(difficulty)
            except util.osu_parser.OsuBeatmapVersionTooOldException or util.osu_parser.OsuFileFormatException:
                pass

        songs.add_song(song)

    print("There are {} song{} in the songs directory.".format(len(songs.songs), "" if len(songs.songs) == 1 else "s"))
    print("")
    print("------------------------------------------------------------------")
    print("")
    print("Matching songs in collection to songs in song folder...")

    # Construct dictionary of {"hash": "beatmap"}
    lookup_dict = {}
    for song in songs.songs:
        for diff in song.difficulties:
            lookup_dict[diff.hash] = diff

    matched = 0
    unmatched = 0

    for collection in collections.collections:
        for diff in collection.beatmaps:
            try:
                diff.difficulty = lookup_dict[diff.hash]
                matched += 1
            except KeyError:
                unmatched += 1

    print("Matched {} hashes to songs, could not match {} hashes.".format(matched, unmatched))
    print("")
    print("------------------------------------------------------------------")
    print("")
    for collection in collections.collections:
        print("Collection {}:".format(collection.name))
        for song in collection.beatmaps:
            if song.difficulty:
                print("|- {}".format(song.difficulty.name))
            else:
                print("|- {} [UNMATCHED]".format(song.hash))




