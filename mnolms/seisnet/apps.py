from django.apps import AppConfig


class BasicinfoConfig(AppConfig):
    name = 'seisnet'

    def ready(self):
        import seisnet.singals
