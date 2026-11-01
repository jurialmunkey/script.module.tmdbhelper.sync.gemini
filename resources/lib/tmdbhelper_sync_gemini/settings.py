from xbmcaddon import Addon


class GeminiSettings:
    addon_id = 'script.module.tmdbhelper.sync.gemini'

    def __init__(self):
        self.addon = Addon(self.addon_id)

    @property
    def api_key(self):
        return self.addon.getSetting('apikey')

    def migrate_settings(self):
        legacy_addon = Addon('plugin.video.themoviedb.helper')
        legacy_key = legacy_addon.getSetting('gemini_apikey')
        if not legacy_key:
            return
        destination_key = self.api_key or legacy_key
        if not self.api_key:
            self.addon.setSetting('apikey', destination_key)
        if self.api_key != destination_key:
            raise RuntimeError('Unable to save migrated Gemini API key')
        legacy_addon.setSetting('gemini_apikey', '')
        if legacy_addon.getSetting('gemini_apikey'):
            raise RuntimeError('Unable to clear legacy Gemini API key')
