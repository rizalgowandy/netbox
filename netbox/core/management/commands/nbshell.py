import code
import platform
import sys

from django import get_version
from django.apps import apps
from django.conf import settings
from django.core.management.base import BaseCommand

from core.models import ObjectType
from users.models import User

APPS = ('circuits', 'core', 'dcim', 'extras', 'ipam', 'tenancy', 'users', 'virtualization', 'vpn', 'wireless')
EXCLUDE_MODELS = (
    'extras.branch',
    'extras.stagedchange',
)

BANNER_TEXT = """### NetBox interactive shell ({node})
### Python {python} | Django {django} | NetBox {netbox}
### lsmodels() will show available models. Use help(<model>) for more info.""".format(
    node=platform.node(),
    python=platform.python_version(),
    django=get_version(),
    netbox=settings.RELEASE.name
)


class Command(BaseCommand):
    help = "Start the Django shell with all NetBox models already imported"
    django_models = {}

    def add_arguments(self, parser):
        parser.add_argument(
            '-c', '--command',
            help='Python code to execute (instead of starting an interactive shell)',
        )

    def _lsmodels(self):
        for app, models in self.django_models.items():
            app_name = apps.get_app_config(app).verbose_name
            print(f'{app_name}:')
            for m in models:
                print(f'  {m}')

    def get_namespace(self):
        namespace = {}

        # Gather Django models and constants from each app
        for app in APPS:
            models = []

            # Load models from each app
            for model in apps.get_app_config(app).get_models():
                app_label = model._meta.app_label
                model_name = model._meta.model_name
                if f'{app_label}.{model_name}' not in EXCLUDE_MODELS:
                    namespace[model.__name__] = model
                    models.append(model.__name__)
            self.django_models[app] = sorted(models)

            # Constants
            try:
                app_constants = sys.modules[f'{app}.constants']
                for name in dir(app_constants):
                    namespace[name] = getattr(app_constants, name)
            except KeyError:
                pass

        # Additional objects to include
        namespace['ObjectType'] = ObjectType
        namespace['User'] = User

        # Load convenience commands
        namespace.update({
            'lsmodels': self._lsmodels,
        })

        return namespace

    def handle(self, **options):
        namespace = self.get_namespace()

        # If Python code has been passed, execute it and exit.
        if options['command']:
            exec(options['command'], namespace)
            return

        # Try to enable tab-complete
        try:
            import readline
            import rlcompleter
        except ModuleNotFoundError:
            pass
        else:
            readline.set_completer(rlcompleter.Completer(namespace).complete)
            readline.parse_and_bind('tab: complete')

        # Run interactive shell
        shell = code.interact(banner=BANNER_TEXT, local=namespace)
        return shell
