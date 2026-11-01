from xbmcaddon import Addon
from xbmcvfs import translatePath


ADDONPATH = translatePath(Addon('script.module.tmdbhelper.sync.gemini').getAddonInfo('path'))


def get_icon(name='gemini'):
    return f'{ADDONPATH}/resources/icons/gemini/{name}.png'
