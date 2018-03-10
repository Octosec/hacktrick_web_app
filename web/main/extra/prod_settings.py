import environ
env = environ.Env(DEBUG=(bool, False),)
environ.Env.read_env()


DATABASES = {
    'default': env.db()
}

SECRET_KEY = env('SECRET_KEY')

DEBUG = False

BROKER_URL = "amqp://guest:guest@rabbitmq:5672//"
