# from decouple import config

import os
config = lambda x: os.getenv(x)


CLIENT_ID = config('CLIENT_ID')
CLIENT_SECRET = config('CLIENT_SECRET')
REDIRECT_URI = config('REDIRECT_URI')
