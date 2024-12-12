import os
from dotenv import load_dotenv

load_dotenv(".env")
YT_DOWNLOAD_PATH = os.getenv('YT_DOWNLOAD_PATH')
DISCORD_TOKEN = os.getenv('DISCORD_TOKEN')
COOKIES_FROM_BROWSER = os.getenv('COOKIES_FROM_BROWSER')