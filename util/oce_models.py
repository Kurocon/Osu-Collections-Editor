import logging


class Collections:
    """
    :type version: int
    :type collections: list[Collection]
    """
    def __init__(self):
        self.version = 0
        self.collections = []

    def set_collection(self, name, collection):
        try:
            c = [c for c in self.collections if c.name == name][0]
        except KeyError:
            c = None

        if c is not None:
            i = self.collections.index(c)
            self.collections[i] = collection
        else:
            self.collections.append(collection)

    def get_collection(self, name):
        try:
            c = [c for c in self.collections if c.name == name][0]
        except KeyError:
            c = None

        return c


class Collection:
    """
    :type name: str
    :type beatmaps: list[CollectionMap]
    :type mapsets: list[Song]
    :type unmatched: list[CollectionMap]
    """
    def __init__(self):
        self.name = ""
        self.beatmaps = []
        self.mapsets = []
        self.unmatched = []

    def get_unmatched_song(self, song_hash):
        """
        Returns CollectionMap of the given unmatched hash
        :param song_hash:
        :return:
        """
        for s in self.unmatched:
            if s.hash == song_hash:
                return s
        return None

    def find_collectionmap_by_difficulty(self, difficulty_or_hash):
        """
        Finds the collectionmap object beloning to the given difficulty
        :param difficulty_or_hash: The difficulty or hash to search for
        :type difficulty_or_hash: Difficulty2|str
        :return: The collectionmap if found, else None
        :rtype: CollectionMap|None
        """
        if isinstance(difficulty_or_hash, str):
            for m in self.beatmaps:
                if m.hash == difficulty_or_hash:
                    return m
            else:
                return None
        elif isinstance(difficulty_or_hash, Difficulty2):
            for m in self.beatmaps:
                if m.difficulty == difficulty_or_hash:
                    return m
            else:
                return None
        else:
            return None

    def remove_song(self, song_difficulty_or_hash):
        found = None
        for m in self.beatmaps:
            if isinstance(song_difficulty_or_hash, str):
                if m.hash == song_difficulty_or_hash:
                    found = m
                    break
            elif isinstance(song_difficulty_or_hash, Difficulty2):
                if m.difficulty == song_difficulty_or_hash or m.hash == song_difficulty_or_hash.hash:
                    found = m
                    break

        if found:
            # Remove the map from the beatmap list
            self.beatmaps.remove(found)

            # We also need to remove the map from the mapset it belongs to
            for m in self.mapsets:
                if found.difficulty.hash in [d.hash for d in m.difficulties]:
                    # If the found difficulty is the same, remove it directly
                    if found.difficulty in m.difficulties:
                        m.difficulties.remove(found.difficulty)
                    # Else, find the entry in the list by hash, then remove it.
                    else:
                        for d in m.difficulties:
                            if d.hash == found.difficulty.hash:
                                m.difficulties.remove(d)
                                break

                    # If there are no maps in this mapset any more, remove it
                    if not m.difficulties:
                        self.mapsets.remove(m)
            return True
        else:
            # The song was not found in this collections' beatmaps. Try to remove it from the mapsets if it is in there.
            if isinstance(song_difficulty_or_hash, Difficulty2):
                for m in self.mapsets:
                    if song_difficulty_or_hash.hash in [d.hash for d in m.difficulties]:
                        for d in m.difficulties:
                            if d.hash == song_difficulty_or_hash.hash:
                                m.difficulties.remove(d)
                                break

                        # If there are no maps in this mapset any more, remove it
                        if not m.difficulties:
                            self.mapsets.remove(m)

            return False


class CollectionMap:
    """
    :type hash: str
    :type difficulty: Difficulty2
    :type mapset: Song
    :type from_api: bool
    """
    def __init__(self):
        self.hash = ""
        self.difficulty = None
        self.mapset = None
        self.from_api = False


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
        from util.osu_parser import parse_osu_file
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
        self.beatmapset_id = ""

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
        from util.osu_parser import md5, parse_osu_file
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
