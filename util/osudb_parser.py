import hashlib
import os
import re
import logging
import traceback

from util.oce_models import Difficulty2, Songs, Song
from util.osudb_format import OSU_SINGLE, OSU_SHORT, OSU_LONG, OSU_BOOLEAN, OSU_BYTE, OSU_DOUBLE, OSU_INT
from util.osudb_format import read_type

# osu!.db format
# Data type     Description
# Int           osu! version (e.g. 20150203)
# Int           Folder Count
# Bool          AccountUnlocked (only false when account is locked or banned in any way)
# DateTime      Date the account will be unlocked
# String        Player name
# Int           Number of beatmaps
# Beatmaps*     The beatmaps themselves

# Beatmap Format
# String            Artist name
# String            Artist name, Unicode
# String            Song title
# String            Song title, Unicode
# String            Creator name
# String            Difficulty name
# String            Audio file name
# String            MD5 hash of map
# String            Name of .osu file for map
# Byte              Ranked status (4=ranked, 5=approved, 2=pending/graveyard)
# Short             Number of hitcircles
# Short             Number of sliders
# Short             Number of spinners
# Long              Last modification time in windows ticks
# Byte/Single       Approach rate (Byte if version is less than 20140609, Single otherwise)
# Byte/Single       Circle size (Byte if version is less than 20140609, Single otherwise)
# Byte/Single       HP drain (Byte if version is less than 20140609, Single otherwise)
# Byte/Single       Overall Difficulty (Byte if version is less than 20140609, Single otherwise)
# Double            Slider velocity
# Int-Doublepair*   An int indicating the number of following Int-Double pairs, then the pairs themselves.
#                   Star rating info for osu!standard. The int is the mod combination, the Double is the star rating.
#                   Only present if version greater or equal to 20140609.
# Int-Doublepair*   An int indicating the number of following Int-Double pairs, then the pairs themselves.
#                   Star rating info for Taiko. The int is the mod combination, the Double is the star rating.
#                   Only present if version greater or equal to 20140609.
# Int-Doublepair*   An int indicating the number of following Int-Double pairs, then the pairs themselves.
#                   Star rating info for CTB. The int is the mod combination, the Double is the star rating.
#                   Only present if version greater or equal to 20140609.
# Int-Doublepair*   An int indicating the number of following Int-Double pairs, then the pairs themselves.
#                   Star rating info for osu!mania. The int is the mod combination, the Double is the star rating.
#                   Only present if version greater or equal to 20140609.
# Int               Drain time in seconds
# Int               Total time in milliseconds
# Int               Time when audio preview starts in ms
# Timingpoint+      An int indicating the number of Timingpoints, then the timingpoints.
# Int               Beatmap ID
# Int               Beatmap set ID
# Int               Thread ID
# Byte              Grade achieved in osu!Standard
# Byte              Grade achieved in Taiko
# Byte              Grade achieved in CTB
# Byte              Grade achieved in osu!Mania
# Short             Local beatmap offset
# Single            Stack leniency
# Byte              Osu gameplay mode. 0x00=standard, 0x01=Taiko, 0x02=CTB, 0x03=Mania
# String            Song source
# String            Song tags
# Short             Online offset
# String            Font used for the title of the song
# Boolean           Is the beatmap unplayed
# Long              Last time played
# Boolean           Is beatmap osz2
# String            Folder name of beatmap, relative to Songs folder
# Long              Last time when map was checked with osu! repo
# Boolean           Ignore beatmap sounds
# Boolean           Ignore beatmap skin
# Boolean           Disable storyboard
# Boolean           Disable video
# Boolean           Visual override
# Short?            Unknown. Only present when version less than 20140609
# Int               Unknown. Some last modification time or something
# Byte              Mania scroll speed


def parse_beatmap(fobj, version):
    log = logging.getLogger(__name__)
    # First, the trivial data of the beatmap
    data = []
    for type in ["String"]*9 + ["Byte"] + ["Short"]*3 + ["Long"]:
        data.append(read_type(type, fobj))
    artist, artist_u, song, song_u, creator, difficulty, audio_file, md5, osu_file, ranked_status, num_hitcircles, num_sliders, num_spinners, last_modified = data

    log.log(5, "artist:{}, artist_u:{}, song:{}, song_u:{}, creator:{}, difficulty:{}, audio_file:{}, "
              "md5:{}, osu_file:{}, ranked_status:{}, num_hitcircles:{}, num_sliders:{}, num_spinners:{}, "
              "last_modified:{}".format(artist, artist_u, song, song_u, creator, difficulty, audio_file,
                                        md5, osu_file, ranked_status, num_hitcircles, num_sliders, num_spinners,
                                        last_modified))

    # Then, the ar, cs, hp and od. If the version is less than 20140609, we need to read 4 bytes, else, 4 singles.
    data = []

    if version < 20140609:
        types = ["Byte"]*4
    else:
        types = ["Single"]*4

    for type in types:
        data.append(read_type(type, fobj))

    ar, cs, hp, od = data

    # Then, the slider velocity
    slider_velocity = read_type("Double", fobj)

    log.log(5, "ar:{}, cs:{}, hp:{}, od:{}, slider_velocity:{}".format(ar, cs, hp, od, slider_velocity))

    # Then the star ratings. These are an int, followed by that many Int-Double pairs.
    data = []
    for type in ["IntDoublepair"]*4:
        num_idp = read_type("Int", fobj)
        idps = []
        for _ in range(num_idp):
            idps.append(read_type(type, fobj))
        data.append(idps)
    stars_standard, stars_taiko, stars_ctb, stars_mania = data

    log.log(5, "stars_standard:{}, stars_taiko:{}, stars_ctb:{}, stars_mania:{}".format(stars_standard, stars_taiko,
                                                                                       stars_ctb, stars_mania))

    # Then, the drain time, total time and preview times
    drain_time = read_type("Int", fobj)
    total_time = read_type("Int", fobj)
    preview_time = read_type("Int", fobj)

    log.log(5, "draintime:{}, totaltime:{}, previewtime:{}".format(drain_time, total_time, preview_time))

    # Then, the timing points. These are an int followed by that many Timingpoints.
    num_timingpoints = read_type("Int", fobj)
    log.debug("There are {} timingpoints.".format(num_timingpoints))
    timingpoints = []
    for _ in range(num_timingpoints):
        timingpoints.append(read_type("Timingpoint", fobj))

    log.log(5, "timing_points: {}".format(timingpoints))

    # Then some more trivial data
    data = []
    for type in ["Int"]*3 + ["Byte"]*4 + ["Short", "Single", "Byte"] + ["String"]*2 + ["Short", "String", "Boolean", "Long", "Boolean", "String", "Long"] + ["Boolean"]*5:
        data.append(read_type(type, fobj))
    beatmap_id, beatmap_set_id, thread_id, grade_standard, grade_taiko, grade_ctb, grade_mania, local_offset, stack_leniency, gameplay_mode, source, tags, online_offset, font, unplayed, last_played, is_osz2, beatmap_folder, last_checked, ignore_sounds, ignore_skin, disable_storyboard, disable_video, visual_override = data

    log.log(5, "beatmap_id:{}, beatmap_set_id:{}, thread_id:{}, grade_standard:{}, grade_taiko:{}, grade_ctb:{}, "
              "grade_mania:{}, local_offset:{}, stack_leniency:{}, gameplay_mode:{}, source:{}, tags:{}, "
              "online_offset:{}, font:{}, unplayed:{}, last_played:{}, is_osz2:{}, beatmap_folder:{}, "
              "last_checked:{}, ignore_sounds:{}, ignore_skin:{}, disable_storyboard:{}, disable_video:{}, "
              "visual_override:{}".format(beatmap_id, beatmap_set_id, thread_id, grade_standard, grade_taiko, grade_ctb,
                                       grade_mania, local_offset, stack_leniency, gameplay_mode, source, tags,
                                       online_offset, font, unplayed, last_played, is_osz2, beatmap_folder,
                                       last_checked, ignore_sounds, ignore_skin, disable_storyboard, disable_video,
                                       visual_override))

    # Then a short which is only there if the version is less than 20140609
    if version < 20140609:
        some_short = read_type("Short", fobj)
        log.log(5, "some_short:{}".format(some_short))

    # Then, lastly, some last modification time and the mania scroll speed
    unknown_int_modified = read_type("Int", fobj)
    mania_scroll_speed = read_type("Byte", fobj)

    log.log(5, "unknown_int_modified:{}, mania_scroll_speed:{}".format(unknown_int_modified, mania_scroll_speed))

    # Now, extract only the parts we need from the beatmap and construct a nice Difficulty2 object.
    beatmap = Difficulty2("")
    beatmap.path = osu_file
    beatmap.name = song
    beatmap.artist = artist
    beatmap.mapper = creator
    beatmap.difficulty = difficulty
    beatmap.ar = ar
    beatmap.cs = cs
    beatmap.hp = hp
    beatmap.od = od
    beatmap.hash = md5
    beatmap.from_api = False
    beatmap.api_beatmap_id = beatmap_id
    beatmap.beatmap_id = beatmap_id
    beatmap.beatmapset_id = beatmap_set_id

    log.debug("Loaded {}: {} - {} [{}] by {}".format(beatmap.beatmap_id, beatmap.artist,
                                                     beatmap.name, beatmap.difficulty, beatmap.mapper))

    return beatmap


def load_osudb(path):
    log = logging.getLogger(__name__)
    log.debug("Opening file {}".format(path))
    fobj = open("{}".format(path), 'rb')

    songs = Songs()

    # Try to parse the file as an osu db.

    # First we have some primitive simple types we can just read in one bunch
    data = []
    for type in ["Int", "Int", "Boolean", "DateTime", "String", "Int"]:
        data.append(read_type(type, fobj))

    version, num_folders, unlocked, unlock_time, player_name, num_maps = data

    log.debug("osu!DB version {}. {} maps".format(version, num_maps))
    log.log(5, "num_folders: {}, unlocked: {}, unlock_time: {}, player_name: {}".format(
        num_folders, unlocked, unlock_time, player_name
    ))

    # Then, for each beatmap, we need to read the beatmap
    beatmaps = []
    for _ in range(num_maps):
        beatmaps.append(parse_beatmap(fobj, version))

    # Now, group the beatmaps by their mapset id, to group them into Songs for the songs list.
    mapsets = {}
    for map in beatmaps:
        if map.beatmapset_id in mapsets.keys():
            mapsets[map.beatmapset_id].append(map)
        else:
            mapsets[map.beatmapset_id] = [map]

    # Create Songs from the mapsets.
    for mapset in mapsets.values():
        s = Song()
        s.difficulties = mapset
        songs.add_song(s)

    return songs


def load_osudb_gui(path, dialog):
    log = logging.getLogger(__name__)
    log.debug("Opening file {}".format(path))
    fobj = open("{}".format(path), 'rb')

    songs = Songs()
    num_done = 0

    dialog.progress.emit(0)
    dialog.current.emit("Parsing metadata...")

    # Try to parse the file as an osu db.
    # First we have some primitive simple types we can just read in one bunch
    data = []
    for type in ["Int", "Int", "Boolean", "DateTime", "String", "Int"]:
        data.append(read_type(type, fobj))

    version, num_folders, unlocked, unlock_time, player_name, num_maps = data

    log.debug("osu!DB version {}. {} maps".format(version, num_maps))
    log.log(5, "num_folders: {}, unlocked: {}, unlock_time: {}, player_name: {}".format(
        num_folders, unlocked, unlock_time, player_name
    ))

    # Then, for each beatmap, we need to read the beatmap
    beatmaps = []
    dialog.current.emit("Parsing beatmaps...")
    for _ in range(num_maps):
        dialog.progress.emit(int((num_done / num_maps) * 100))
        beatmaps.append(parse_beatmap(fobj, version))
        num_done += 1

    dialog.current.emit("Loading mapsets into OCE...")

    # Now, group the beatmaps by their mapset id, to group them into Songs for the songs list.
    mapsets = {}
    for map in beatmaps:
        if map.beatmapset_id in mapsets.keys():
            mapsets[map.beatmapset_id].append(map)
        else:
            mapsets[map.beatmapset_id] = [map]

    # Create Songs from the mapsets.
    for mapset in mapsets.values():
        s = Song()
        s.difficulties = mapset
        songs.add_song(s)

    dialog.progress.emit(100)

    return songs
