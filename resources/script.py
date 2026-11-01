from xbmc import executebuiltin


if __name__ == '__main__':
    executebuiltin(
        'RunScript(plugin.video.themoviedb.helper,open_sync_provider_settings,'
        'addon_id=script.module.tmdbhelper.sync.gemini)')
