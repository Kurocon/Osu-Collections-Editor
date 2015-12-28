from pprint import pprint

from util.osu_api import get_beatmap_by_hash

if __name__ == "__main__":
    maphash = "921f3ed9bd3af0d960d11108b61a9dcb"

    print("Trying to find beatmap with hash {}".format(maphash))
    mapinfo = get_beatmap_by_hash(maphash)

    pprint(mapinfo)
