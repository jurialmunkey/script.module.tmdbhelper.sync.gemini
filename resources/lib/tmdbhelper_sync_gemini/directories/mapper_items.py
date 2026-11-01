from jurialmunkey.ftools import cached_property
from tmdbhelper.lib.addon.plugin import get_localized
from tmdbhelper.lib.items.directories.mapper_basic import ItemMapper


class GeminiItemMapper(ItemMapper):
    @cached_property
    def tmdb_type(self):
        return 'movie' if self.meta['recommendation']['type'] == 'Movie' else 'tv'

    @cached_property
    def reason(self):
        return self.meta['recommendation'].get('reason') or ''

    def get_infolabels(self):
        return {'mediatype': 'movie' if self.tmdb_type == 'movie' else 'tvshow'}

    def get_infoproperties(self):
        return {
            'plot_affix': f'[B]Gemini {get_localized(32223)}:[/B] {self.reason}[CR]',
            'reason': self.reason,
        }

    def get_unique_ids(self):
        return {'tmdb': self.meta['tmdb_id']}

    def get_params(self):
        return {
            'info': 'details',
            'tmdb_type': self.tmdb_type,
            'tmdb_id': self.meta['tmdb_id'],
        }
