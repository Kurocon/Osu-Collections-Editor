import logging


class Settings:
    """
    Storage class for application settings
    :type osu_api_key: str
    :type default_songs_dir: str
    :type default_collection_file: str
    """

    _instance = None

    def __init__(self):
        self.log = logging.getLogger(__name__)
        self.settings = {
            'osu_api_key': "11a8e6022b8146bbcaf2a9085fddf5232feaaee2"
        }

    def get_setting(self, name):
        res = self.settings.get(name, None)
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
