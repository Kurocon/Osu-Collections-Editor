import hashlib
import os
import re
import logging
import traceback

from util.oce_models import Difficulty2, Song, Songs

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


def parse_osu_file(path):
    log.debug("Reading .osu file {}".format(path))
    log.debug("Opening file {}".format(path))
    fobj = open("{}".format(path), 'r', encoding='utf8')

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
