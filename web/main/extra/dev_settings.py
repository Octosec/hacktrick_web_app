DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'postgres',
        'USER': 'postgres',
        'PASSWORD': 'postgres',
        'HOST': 'db',
        'PORT': '5432'
    }
}

CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": "redis://redis/",
        'TIMEOUT': 60,
        "OPTIONS": {
            'MAX_ENTRIES': 1000,
            'server_max_value_length': 1024 * 1024 * 2,
            "DB": 1,
            "CLIENT_CLASS": "django_redis.client.DefaultClient"
        },
        "KEY_PREFIX": "hattrick"
    }
}

DEBUG = True

BROKER_URL = "amqp://guest:guest@rabbitmq:5672//"
