import requests

import settings

"""
Interface for the Osu! API.
"""


def get_beatmap_by_hash(map_hash):
    payload = {
        'k': settings.osu_api_key,
        'h': map_hash
    }
    r = requests.get('https://osu.ppy.sh/api/get_beatmaps', params=payload)

    return r.json()
