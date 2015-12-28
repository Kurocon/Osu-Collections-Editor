import util.collections_parser

if __name__ == "__main__":

    default_path = "/data/OwnCloud/Osu Program/collection.db"

    print("------------------------------------------------------------------")
    print(" Osu Collections DB Parser Test")
    print("------------------------------------------------------------------")
    print("Input the path to your OSU! collection.db, or enter to use the default.")
    print("The default is \"{}\"".format(default_path))
    path = input("Path: ")

    if not path:
        path = default_path

    print("")
    print("You have typed {} as the path.".format(path))
    print("------------------------------------------------------------------")

    collections = util.collections_parser.parse_collections(path)
    ccount = collections.collection_count
    print("There are {} collection{} in this database:".format(ccount, "" if ccount == 1 else "s"))

    for c in collections.collections:
        print("- {} ({} map{})".format(c.name, c.beatmap_count, "" if c.beatmap_count == 1 else "s"))
