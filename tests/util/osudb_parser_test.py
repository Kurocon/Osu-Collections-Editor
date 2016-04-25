import util.osudb_parser
from logging.config import fileConfig, logging

if __name__ == "__main__":
    fileConfig('../../logging.conf')
    log = logging.getLogger(__name__)
    log.debug("Debugging mode enabled...")
    log.info("osu!DB test starting...")

    default_path = "/data/OwnCloud/Osu Program/osu!.db"

    print("------------------------------------------------------------------")
    print(" Osu! DB Parser Test")
    print("------------------------------------------------------------------")
    print("Input the path to your osu!.db, or enter to use the default.")
    print("The default is \"{}\"".format(default_path))
    path = input("Path: ")

    if not path:
        path = default_path

    print("")
    print("You have typed {} as the path.".format(path))
    print("------------------------------------------------------------------")

    songs = util.osudb_parser.load_osudb(path)
    scount = len(songs.songs)
    print("There are {} song{} in this database:".format(scount, "" if scount == 1 else "s"))

    for s in songs.songs:
        print("- {}".format(s))
