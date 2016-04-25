import sys
from pprint import pprint

from util.osu_parser import find_songs
from util.oce_models import Difficulty2, Song

if __name__ == "__main__":

    default_path = "/data/OwnCloud/Osu Songs/"

    print("------------------------------------------------------------------")
    print(" Osu Parser Test")
    print("------------------------------------------------------------------")
    print("Input your OSU! music directory path, or enter to use the default.")
    print("The default is \"{}\"".format(default_path))
    path = input("Path: ")

    if not path:
        path = default_path

    print("")
    print("You have typed {} as the path.".format(path))
    print("------------------------------------------------------------------")

    # Find first song
    song_dirs = find_songs(path)
    sorted_song_dirs = sorted(song_dirs)

    song = None
    difficulty = None
    song_id = 0
    while not difficulty:
        if len(sorted_song_dirs) > song_id:
            song = sorted_song_dirs[song_id]
        else:
            print("There are no usable songs in this directory. Please restart and use a proper dir.")
            sys.exit(1)

        diffs = song_dirs.get(song)
        sorted_diffs = sorted(diffs)
        if len(sorted_diffs) > 0:
            difficulty = sorted_diffs[0]
        else:
            song_id += 1
            print("Cannot use song {}, no difficulties.".format(song))

    print("------------------------------------------------------------------")
    print("Using song: {}".format(song))
    print("Using difficulty: {}".format(difficulty))

    beatmap_diff = Difficulty2.from_file("/".join([path, song, difficulty]))
    beatmap = Song()
    beatmap.add_difficulty(beatmap_diff)

    print("------------------------------------------------------------------")
    print("Beatmap: {}".format(beatmap_diff.get_path()))
    pprint(beatmap_diff.get_data())
