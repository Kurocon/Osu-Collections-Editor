import hashlib
import os
import re
import logging
import traceback

log = logging.getLogger(__name__)


def find_songs(songs_directory):
    log.debug("Using song directory {}".format(songs_directory))
    songs = {}
    for folder in [d for d in os.listdir(songs_directory) if os.path.isdir(songs_directory + "/"+d)]:
        log.debug("Checking subfolder {}".format(folder))
        files = [f for f in os.listdir(songs_directory + "/" + folder) if f.endswith(".osu")]
        log.debug("Found {} difficulties in folder {}.".format(len(files), folder))
        songs[folder] = files

    return songs


sectionPattern = re.compile(r'^\[([a-zA-Z0-9]+)\]$')
keyvalPattern = re.compile(r'^([a-zA-Z0-9]+)\s*:\s*(.*)$')
osuversionPattern = re.compile(r'^[\s\ufeff\x7f]*osu file format v([0-9]+)\s*$')
blanklinePattern = re.compile(r'^[\s\ufeff\x7f]*$')


class OsuFileFormatException(Exception):
    pass


class OsuBeatmapVersionTooOldException(Exception):
    pass


class Difficulty:
    """
    :type path: str
    :type data: dict
    """
    def __init__(self, path, data):
        self.path = path
        self.data = data

    def get_data(self):
        return self.data

    def get_path(self):
        return self.path

    def get_version(self):
        return self.data["version"]

    def get_difficulty(self, key=None):
        if key:
            return self.data["Difficulty"][key]
        else:
            return self.data["Difficulty"]

    def get_ar(self):
        return self.data["Difficulty"]["ApproachRate"]

    def get_cs(self):
        return self.data["Difficulty"]["CircleSize"]

    def get_hp(self):
        return self.data["Difficulty"]["HPDrainRate"]

    def get_od(self):
        return self.data["Difficulty"]["OverallDifficulty"]

    def get_slider_multiplier(self):
        return self.data["Difficulty"]["SliderMultiplier"]

    def get_slider_tick_rate(self):
        return self.data["Difficulty"]["SliderTickRate"]

    def get_editor(self, key=None):
        if key:
            return self.data["Editor"][key]
        else:
            return self.data["Editor"]

    def get_general(self, key=None):
        if key:
            return self.data["General"][key]
        else:
            return self.data["General"]

    def get_audio_filename(self):
        return self.data["General"]["AudioFilename"]

    def get_audio_path(self):
        return "{}/{}".format(os.path.dirname(self.path), self.data["General"]["AudioFilename"])

    def get_audio_lead_in(self):
        return self.data["General"]["AudioLeadIn"]

    def get_countdown(self):
        return self.data["General"]["Countdown"]

    def get_mode(self):
        return self.data["General"]["Mode"]

    def get_artist(self):
        return self.data["Metadata"]["Artist"]

    def get_unicode_artist(self):
        return self.data["Metadata"]["ArtistUnicode"]

    def get_beatmap_id(self):
        return self.data["Metadata"]["BeatmapID"]

    def get_beatmap_set_id(self):
        return self.data["Metadata"]["BeatmapSetID"]

    def get_creator(self):
        return self.data["Metadata"]["Creator"]

    def get_source(self):
        return self.data["Metadata"]["Source"]

    def get_tags(self):
        return self.data["Metadata"]["Tags"]

    def get_title(self):
        return self.data["Metadata"]["Title"]

    def get_unicode_title(self):
        return self.data["Metadata"]["TitleUnicode"]

    def get_difficulty_string(self):
        return self.data["Metadata"]["Version"]

    def get_difficulty_multiplier(self):
        cs = int(self.get_cs())
        od = int(self.get_od())
        hp = int(self.get_hp())

        return cs+od+hp

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        return "Diff: {} - {} ({}) [{}]".format(self.get_artist(), self.get_title(),
                                                self.get_creator(), self.get_version())

    @classmethod
    def from_file(cls, filepath):
        return cls(filepath, parse_osu_file(filepath))


class Difficulty2:
    """
    :type path: str
    :type hash: str
    """
    def __init__(self, path):
        self.path = path
        self.name = ""
        self.artist = ""
        self.mapper = ""
        self.difficulty = ""
        self.ar = 0.0
        self.cs = 0.0
        self.hp = 0.0
        self.od = 0.0
        self.hash = ""
        self.from_api = False
        self.api_beatmap_id = ""
        self.beatmap_id = ""

    def deep_copy(self):
        res = Difficulty2("")
        for attr in ["path", "name", "artist", "mapper", "difficulty", "ar", "cs", "hp", "od", "hash", "from_api"]:
            setattr(res, attr, getattr(self, attr))
        return res

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        return "Diff2: {} - {} ({}) [{}]".format(self.artist, self.name, self.mapper, self.difficulty)

    @classmethod
    def from_file(cls, path):
        d = cls(path)
        d.hash = md5(path)

        details = parse_osu_file(path)
        d.name = details["Metadata"]["Title"]
        d.artist = details["Metadata"]["Artist"]
        d.mapper = details["Metadata"]["Creator"]
        d.difficulty = details["Metadata"]["Version"]

        try:
            d.beatmap_id = details["Metadata"]["BeatmapID"]
        except KeyError:
            pass

        try:
            d.ar = details["Difficulty"]["ApproachRate"]
        except KeyError:
            pass

        try:
            d.cs = details["Difficulty"]["CircleSize"]
        except KeyError:
            pass

        try:
            d.hp = details["Difficulty"]["HPDrainRate"]
        except KeyError:
            pass

        try:
            d.od = details["Difficulty"]["OverallDifficulty"]
        except KeyError:
            pass

        return d


class Song:
    """
    :type difficulties: list[Difficulty|Difficulty2]
    """
    def __init__(self):
        self.difficulties = []

    def add_difficulty(self, difficulty):
        self.difficulties.append(difficulty)

    def deep_copy(self):
        """
        :rtype: Song
        """
        res = Song()

        if len(self.difficulties) == 0:
            print("Copying song with 0 diffs!")

        # Create deep copies of the diffs and add them
        for d in self.difficulties:
            d_dc = d.deep_copy()
            res.add_difficulty(d_dc)

        return res

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        return "Song ({} difficulties): {}".format(len(self.difficulties), self.difficulties)


class Songs:
    """
    :type songs: list[Song]
    """
    def __init__(self):
        self.songs = []
        self.log = logging.getLogger(__name__)

    def add_song(self, song):
        if not song.difficulties:
            self.log.warning("An empty song was added!")
        self.songs.append(song)

    def get_song(self, song_hash):
        """
        Returns the song with the given hash
        :param song_hash: Hash of the song to get
        :type song_hash: str
        :return: Mapset and song difficulty, or None if nothing was found
        :rtype: tuple(Song, Difficulty2) | None
        """
        for song in self.songs:
            for diff in song.difficulties:
                if diff.hash == song_hash:
                    return song, diff

        return None

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        return "Songs: {}".format(self.songs)


def parse_osu_file(path):
    log.debug("Reading .osu file {}".format(path))
    log.debug("Opening file {}".format(path))
    fobj = open("{}".format(path), encoding="utf8")

    valid = False
    data = {}
    sectiondata = {}
    sectionlist = []
    currentsection = ""

    for line in fobj:

        # Ignore blank lines, skip to the next iteration
        if line == "\n":
            continue

        # Ignore empty lines, skip to the next iteration
        blank = blanklinePattern.findall(line)
        if len(blank) > 0:
            continue

        if data == {} and not valid:

            version = osuversionPattern.findall(line)
            if len(version) > 0:
                valid = True

                data['version'] = int(version[0])
                log.debug("Osu file format version: {}".format(data['version']))

                if data['version'] < 4:
                    raise OsuBeatmapVersionTooOldException
                continue
            else:
                log.error("{} is not a valid .osu file.".format(path))
                log.debug("The line was: {}".format(line))
                raise OsuFileFormatException
        elif not valid:
            log.error("Something went wrong. {} is not a properly formatted .osu file.".format(path))
            log.debug("The line was: {}".format(line))
            raise OsuFileFormatException

        section = sectionPattern.findall(line)
        if len(section) > 0:
            if currentsection != "":
                data[currentsection] = sectionlist if sectionlist != [] else sectiondata

            sectiondata = {}
            sectionlist = []
            currentsection = section[0]
            continue

        # Ignore some sections
        if currentsection in ["Colours", "HitObjects", "TimingPoints", "Events", "General", "Editor"]:
            continue

        # Parse key-value entries
        keyvalue = keyvalPattern.findall(line)
        if len(keyvalue) > 0:
            key, value = keyvalue[0]

            # Parse Difficulty values
            if currentsection == "Difficulty":
                if key in ["ApproachRate", "CircleSize", "HPDrainRate",
                           "OverallDifficulty", "SliderMultiplier", "SliderTickRate"]:
                    sectiondata[key] = float(value)
                else:
                    sectiondata[key] = value

            # Parse metadata values
            elif currentsection == "Metadata":
                if key in ["BeatmapID", "BeatmapSetID"]:
                    sectiondata[key] = int(value)
                elif key == "Tags":
                    sectiondata[key] = value.split()
                else:
                    sectiondata[key] = value

            # Parse other key-values
            else:
                sectiondata[key] = value
            continue

        log.warning("Unknown line: {}".format(line))

    # Save the last section if applicable
    if currentsection != "" and (sectiondata != {} or sectionlist != []):
        data[currentsection] = sectionlist if sectionlist != [] else sectiondata

    log.debug("Parsing of {} completed.".format(path))
    log.debug("data: {}".format(data))
    return data


def md5(fname):
    h = hashlib.md5()
    with open(fname, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            h.update(chunk)
    return h.hexdigest()


def load_songs_from_dir(directory):
    song_dirs = find_songs(directory)
    sorted_song_dirs = sorted(song_dirs)

    songs = Songs()

    for song_str in sorted_song_dirs:
        song = Song()
        difficulties = song_dirs.get(song_str)
        sorted_difficulties = sorted(difficulties)

        if not difficulties:
            log.warning("Song {} has no difficulties, skipping!".format(song_str))
            continue

        for difficulty_str in sorted_difficulties:
            try:
                difficulty = Difficulty2.from_file("/".join([directory, song_str, difficulty_str]))
                song.add_difficulty(difficulty)
            except OsuBeatmapVersionTooOldException or OsuFileFormatException as e:
                log.warning("Something was wrong with the beatmap {}. The error was: {}".format(difficulty_str, e))

        songs.add_song(song)

    return songs


def load_songs_from_dir_gui(directory, dialog):
    song_dirs = find_songs(directory)
    sorted_song_dirs = sorted(song_dirs)

    songs = Songs()

    num_songdirs = len(sorted_song_dirs)
    num_done = 0

    for song_str in sorted_song_dirs:
        dialog.progress.emit(int((num_done/num_songdirs)*100))
        dialog.current.emit(song_str)

        song = Song()
        difficulties = song_dirs.get(song_str)
        sorted_difficulties = sorted(difficulties)

        if not difficulties:
            log.warning("Song {} has no difficulties, skipping!".format(song_str))
            continue

        for difficulty_str in sorted_difficulties:
            try:
                difficulty = Difficulty2.from_file("/".join([directory, song_str, difficulty_str]))
                song.add_difficulty(difficulty)
            except OsuBeatmapVersionTooOldException or OsuFileFormatException as e:
                log.warning("Something was wrong with the beatmap {}. The error was: {}".format(difficulty_str, e))

        if not song.difficulties:
            log.warning("Song {} has no difficulties, skipping!".format(song_str))
            continue

        songs.add_song(song)
        num_done += 1

    return songs
