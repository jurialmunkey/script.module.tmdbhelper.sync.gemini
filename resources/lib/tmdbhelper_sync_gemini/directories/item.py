from jurialmunkey.ftools import cached_property
from tmdbhelper.lib.addon.plugin import get_localized
from tmdbhelper.lib.items.directories.base.basedir_item import BaseDirItem
from tmdbhelper_sync_gemini.directories.artwork import ADDONPATH, get_icon
from tmdbhelper_sync_gemini.settings import GeminiSettings


class GeminiDirectoryItem(BaseDirItem):
    priority = 205
    label_localized = 32149
    label_type = 'suffixed'
    params = {'info': 'gemini_recommendations'}
    types = (None,)

    @property
    def label_suffix(self):
        return get_localized(32223)

    @property
    def enabled(self):
        return bool(GeminiSettings().api_key)

    @cached_property
    def art(self):
        return self.get_art()

    def get_art(self):
        return {'icon': get_icon(), 'landscape': f'{ADDONPATH}/resources/fanart.jpg'}
