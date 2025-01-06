from django.apps import AppConfig


class WirelessConfig(AppConfig):
    name = 'wireless'

    def ready(self):
        from netbox.models.features import register_models
        from . import signals, search  # noqa: F401

        # Register models
        register_models(*self.get_models())
