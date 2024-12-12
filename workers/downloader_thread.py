import json
from time import sleep
import pathlib
from config import YT_DOWNLOAD_PATH, COOKIES_FROM_BROWSER
from threading import Thread
import yt_dlp

from logger import logger

YOUTUBE_URL = 'youtube.com/watch?'

class AudioDownloaderManager():
    def __init__(self) -> None:
        self.threads = []
        self.queue = []
        self._start()

    def _create_thread(self, search_query: str) -> None:
        thread = Thread(target=download_video, args=(search_query,))
        thread.start()

    def _start(self):
        while True:
            if not self.queue:
                sleep(1)
                continue
            search_query = self.queue.pop(0)
            self._create_thread(search_query)

    def queue_download(self, search_query: str) -> None:
        self.queue.append(search_query)

def test_hook(d):
    pass


def download_video(search_query: str) -> str | None:
    pathlib.Path(f'{YT_DOWNLOAD_PATH}/').mkdir(parents=True, exist_ok=True)
    ydl_opts = {
        'format': 'm4a/bestaudio/best',
        'cookiefile': 'cookies.txt',
        'cookiesfrombrowser': (COOKIES_FROM_BROWSER,),
        # ℹ️ See help(yt_dlp.postprocessor) for a list of available Postprocessors and their arguments
        'postprocessors': [{  # Extract audio using ffmpeg
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'm4a',
        }],
        'windowsfilenames': True,
        'restrictfilenames': True,
        'paths': {
            'home': YT_DOWNLOAD_PATH
        },
        'cachedir': 'cacheyt/',
        # 'progress_hooks': [test_hook],
        'extractor_args': {'youtube': {'player_client': ['ios']}},
    }
    filename = None
    yt_id = None
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            final_query = search_query
            if YOUTUBE_URL not in search_query:
                final_query = f"ytsearch1:{search_query}"
                search_results = ydl.extract_info(final_query, download=True)
                entry = search_results['entries'][0]['requested_downloads'][0]
                filename = entry['filepath']
                yt_id = entry['id']
            else:
                search_results = ydl.extract_info(final_query, download=True)
                yt_id = search_results['id']
                filename = search_results['filename']
    except Exception as e:
        logger.error(f"Failed to download video ytsearch:{search_query}: {e}")
    return filename, yt_id