from jurialmunkey.ftools import cached_property
from tmdbhelper.lib.sync.providers.base import SyncProvider
from tmdbhelper_sync_gemini.directories.item import GeminiDirectoryItem
from tmdbhelper_sync_gemini.directories.routes import LIST_ROUTES
from tmdbhelper_sync_gemini.settings import GeminiSettings


class Provider(SyncProvider):
    interface_version = 3
    provider_id = 'gemini'
    display_name = 'Gemini'
    directory_item_class = GeminiDirectoryItem
    list_routes = LIST_ROUTES

    @cached_property
    def api(self):
        return self.get_api()

    def get_api(self):
        from tmdbhelper_sync_gemini.api import Gemini
        return Gemini()

    def migrate_settings(self):
        GeminiSettings().migrate_settings()

    def is_authorized(self):
        return bool(GeminiSettings().api_key)
