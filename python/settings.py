import os

PORT = 9999
MAX_WORKERS = int(os.environ.get('MAX_WORKERS', 20))
MAX_CONCURRENT_RPCS = int(os.environ.get('MAX_CONCURRENT_RPCS', 20))
MEDIA_FOLDER = os.environ.get('MEDIA_FOLDER', '/tmp/downloads')
API_HASH = os.environ.get('API_HASH', '240bcbe9012de5c96210b27da9814ef5')
API_ID = int(os.environ.get('API_ID', 182155))
BOT_ID = os.environ.get('BOT_ID', 'runotwo')
CLIENT_ID = os.environ.get('CLIENT_ID', 'runotwo')
SENTRY_DSN = os.environ.get('SENTRY_DSN')
ADDRESS = os.environ.get('telegram_api_address')
