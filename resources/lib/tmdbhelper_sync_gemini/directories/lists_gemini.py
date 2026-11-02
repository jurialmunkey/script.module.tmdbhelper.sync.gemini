from xbmcgui import Dialog, INPUT_ALPHANUM
from jurialmunkey.ftools import cached_property
from tmdbhelper.lib.addon.dialog import BusyDialog
from tmdbhelper.lib.addon.logger import kodi_log
from tmdbhelper.lib.addon.thread import ParallelThread
from tmdbhelper.lib.items.directories.lists_default import ListDefault, ListProperties
from tmdbhelper_sync_gemini.directories.mapper_items import GeminiItemMapper
from tmdbhelper_sync_gemini.localization import get_localized


class ListGeminiProperties(ListProperties):
    item_mapper_class = GeminiItemMapper
    plugin_name = 'Gemini'
    tmdb_type = 'both'

    @cached_property
    def cache_name(self):
        return self.get_cache_name()

    def get_cache_name(self):
        return f'ListGemini_{self.query}'

    @cached_property
    def items(self):
        return self.get_cached_items() or []

    def get_uncached_items(self):
        with BusyDialog():
            data = self.gemini.get_prompt_recommendations(self.query)
            if not data:
                return
            try:
                recommendations = data['recommendations']
            except (TypeError, KeyError):
                kodi_log('Gemini FAILED: Unable to locate recommendations data', 1)
                return
            with ParallelThread(recommendations, self.get_recommendation_item) as pt:
                return [item for item in pt.queue if item]

    def get_recommendation_item(self, recommendation):
        try:
            title = recommendation['title']
            year = recommendation['year']
            mode = recommendation['type']
        except (TypeError, KeyError):
            kodi_log(f'Gemini INVALID SPEC: {recommendation}', 1)
            return
        if mode not in ('Movie', 'Show'):
            kodi_log(f'Gemini INVALID SPEC: {recommendation}', 1)
            return
        tmdb_type = 'movie' if mode == 'Movie' else 'tv'
        tmdb_id = self.query_database.get_tmdb_id(tmdb_type=tmdb_type, query=title, year=year)
        tmdb_id = tmdb_id or self.query_database.get_tmdb_id(tmdb_type=tmdb_type, query=title)
        if not tmdb_id:
            kodi_log(f'Gemini UNKNOWN ITEM: {recommendation}', 1)
            return
        return self.get_mapped_item({'recommendation': recommendation, 'tmdb_id': tmdb_id})

    def get_mapped_item(self, item, add_infoproperties=None):
        return self.item_mapper_class(item, add_infoproperties).item


class ListGemini(ListDefault):
    list_properties_class = ListGeminiProperties

    @cached_property
    def gemini(self):
        return self.get_gemini()

    def get_gemini(self):
        from tmdbhelper.lib.sync.providers.registry import SyncProviderRegistry
        return SyncProviderRegistry().get_provider('gemini').api

    def configure_list_properties(self, list_properties):
        list_properties = super().configure_list_properties(list_properties)
        list_properties.plugin_name = 'Gemini'
        list_properties.gemini = self.gemini
        list_properties.pagination = False
        return list_properties

    def get_items(self, query=None, **kwargs):
        if not self.gemini.api_key:
            Dialog().ok(
                'Gemini', f"{get_localized(32150)}[CR]"
                f"{get_localized(32151).format('https://aistudio.google.com/app/api-keys')}")
            return
        query = query or Dialog().input(get_localized(32044), type=INPUT_ALPHANUM)
        if not query:
            return
        self.list_properties.query = query
        return self.get_items_finalised()
