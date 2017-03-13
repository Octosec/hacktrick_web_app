from django.apps import AppConfig


class HacktrickConfig(AppConfig):
    name = 'hacktrick'

    def ready(self):
        import hacktrick.signals