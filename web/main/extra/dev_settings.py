DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'hack',
        'USER': 'postgres',
        'PASSWORD': '2855',
        'HOST': 'localhost',
        'PORT': '5432'
    }
}

DEBUG = True

BROKER_URL = "amqp://guest:guest@rabbitmq:5672//"
