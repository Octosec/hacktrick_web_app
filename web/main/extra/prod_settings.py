import environ
env = environ.Env(DEBUG=(bool, False),)
environ.Env.read_env()


DATABASES = {
    'default': env.db()
}

SECRET_KEY = env('SECRET_KEY')

DEBUG = False
