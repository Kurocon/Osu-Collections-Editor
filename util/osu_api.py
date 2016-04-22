import logging

import requests

from settings import Settings

"""
Interface for the Osu! API.
"""


def get_beatmap_by_hash(map_hash):
    settings = Settings.get_instance()
    payload = {
        'k': settings.get_setting("osu_api_key"),
        'h': map_hash
    }
    r = requests.get('https://osu.ppy.sh/api/get_beatmaps', params=payload)
    result = r.json()

    log = logging.getLogger(__name__)

    if result:
        log.debug("Matched {} to {} - {} [{}] ({})".format(map_hash,
                                                           result[0]['artist'],
                                                           result[0]['title'],
                                                           result[0]['version'],
                                                           result[0]['creator']))

    else:
        log.debug("Could not match {}".format(map_hash))

    return r.json()
