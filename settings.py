import logging
import json
import os


class Settings:
    """
    Storage class for application settings
    """

    _instance = None

    # Static variables that are not user-changeable

    # Osu beatmap lookup URL ({0} will be replaced with the beatmap id)
    OSU_BEATMAP_URL = "https://osu.ppy.sh/b/{0}"
    # Bloodcat beatmap search URL ({0} will be replaced with the beatmap id)
    BLOODCAT_SEARCH_URL = "http://bloodcat.com/osu/?q={0}&c=b&s=&m="

    # Dynamic settings loading from file
    def __init__(self):
        self.log = logging.getLogger(__name__)
        self.default_settings = {
            'osu_api_key': "",
            'download_from_api': 0,

            'default_loadfrom': 0,
            'default_osudb': "",
            'default_songs_folder': "",
            'default_collectiondb': "",

            'show_shutdown_dialog': True,
            'show_api_explanation_dialog': True,
            'show_collection_delete_dialog': True,
            'show_remove_song_dialog': True,
            'show_remove_mapset_dialog': True,
        }

        needs_save = False

        if os.path.exists('settings.json'):
            with open('settings.json', 'r', encoding='utf8') as f:
                self.settings = json.load(f)
        else:
            self.settings = {}
            needs_save = True

        # Check if any default settings are missing and set them.
        for key, value in self.default_settings.items():
            if key not in self.settings.keys():
                self.settings[key] = value
                needs_save = True

        if needs_save:
            with open('settings.json', 'w', encoding='utf8') as f:
                json.dump(self.settings, f, sort_keys=True, indent=4)

    def get_setting(self, name, default=None):
        res = self.settings.get(name, default)
        self.log.debug("Getting setting {}: {}".format(name, res))
        return res

    def set_setting(self, name, value):
        self.log.debug("Setting setting {} to {}".format(name, value))
        self.settings[name] = value

    def remove_setting(self, name):
        if name in self.settings.keys():
            self.log.debug("Removing setting {}".format(name))
            del self.settings[name]
        else:
            self.log.debug("Could not remove setting {}, it does not exist".format(name))

    @classmethod
    def get_instance(cls):
        """
        :return: Settings instance
        :rtype: Settings
        """
        if not cls._instance:
            cls._instance = cls()
        return cls._instance
