from tracker.settings.base import *

DEBUG = True
LOCAL = True
HOST = 'http://localhost:8000'

# ETHERSCAN API
ETHSCAN_HOST = "https://api.etherscan.io/api"
ETHSCAN_API_KEY = "C2USV4YSJ5NWVA3SECN9XJ48KF9JJ1EBVJ"
ENVIRONMENT = 'test'

DATABASES = {
  'default': {
    'ENGINE': 'django.db.backends.sqlite3',
    'NAME': os.path.join(BASE_DIR, 'test_db.sqlite3'),
  }
}

# todo: postgresql
