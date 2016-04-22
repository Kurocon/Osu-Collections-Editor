from pprint import pprint

from util.osu_api import get_beatmap_by_hash

if __name__ == "__main__":
    map_hash = "921f3ed9bd3af0d960d11108b61a9dcb"

    print("Trying to find beatmap with hash {}".format(map_hash))
    map_info = get_beatmap_by_hash(map_hash)

    pprint(map_info)
