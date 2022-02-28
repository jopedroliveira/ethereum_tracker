from tracker.settings.base import *

DEBUG = False
LOCAL = True
HOST = 'http://localhost:8000'

# ETHERSCAN API
ETHSCAN_HOST = "https://api.etherscan.io/api"
ETHSCAN_API_KEY = "C2USV4YSJ5NWVA3SECN9XJ48KF9JJ1EBVJ"

# CELERY

BROKER_URL = 'amqp://guest:guest@127.0.0.1:5672//'
# see https://docs.celeryproject.org/en/3.1/getting-started/brokers/sqs.html#caveats
BROKER_TRANSPORT_OPTIONS = {'visibility_timeout': 2700,
                            'max_retries': 2}  # 30 minutes | 2 retries max

CELERY_RESULT_BACKEND = 'rpc'
#: Only add pickle to this list if your broker is secured
#: from unwanted access (see userguide/security.html)
CELERY_ACCEPT_CONTENT = ['pickle']
CELERY_TASK_SERIALIZER = 'pickle'
CELERY_RESULT_SERIALIZER = 'pickle'

# Database
# https://docs.djangoproject.com/en/2.2/ref/settings/#databases

DATABASES = {
  'default': {
    'ENGINE': 'django.db.backends.sqlite3',
    'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
  }
}

# todo: postgresql
