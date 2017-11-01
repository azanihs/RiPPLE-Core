from os import path
import shutil
from django.core.management.base import BaseCommand


ALLOWED_ENVIRONMENTS = ["production", "testing", "development"]


class Command(BaseCommand):
    help = 'Changes development environment'

    def copy_to(self, environment_name):
        new_config = path.abspath(path.dirname(
            __file__) + '../../../../.' + environment_name + '.env')

        if not path.isfile(new_config):
            raise Exception("File: '" + new_config + "' not found")

        target_location = path.abspath(path.dirname(
            __file__) + '../../../../.current.env')

        shutil.copyfile(new_config, target_location)

    def add_arguments(self, parser):
        # Positional arguments
        parser.add_argument("devenv", nargs='?',
                            type=str, choices=ALLOWED_ENVIRONMENTS)

    def handle(self, *args, **options):
        development_environment = options["devenv"]
        if development_environment not in ALLOWED_ENVIRONMENTS:
            raise Exception(
                "Invalid environment argument provided. Must be " + ALLOWED_ENVIRONMENTS)

        self.copy_to(development_environment)
        print("\n-\nSwitched to environment: " +
              development_environment + "!\n-\n")
