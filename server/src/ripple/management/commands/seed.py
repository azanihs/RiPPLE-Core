from django.core.management.base import BaseCommand
from .seedCourse import Command as CourseSeedCommand
import os

class Command(BaseCommand):
    args = ''
    help = 'Wrapper around the course seeder command'

    def add_arguments(self, parser):
        parser.add_argument("--host")
        parser.add_argument("--dataset", required=True)

    def handle(self, *args, **options):
        host = options.get("host", None)
        json_path = options.get("dataset", None)

        if host is None:
            host = "//localhost:8000"

        course_seeder = CourseSeedCommand(self)
        base_path = os.path.abspath(json_path)
        course_ids = []
        course_names = []
        file_names = []

        for file_name in os.listdir(base_path):
            if not file_name.endswith(".json"):
                continue

            name = file_name.split(".")[0]
            course_ids.append(name)
            course_names.append(name)
            file_names.append(os.path.join(base_path, file_name))

        return course_seeder.handle(args, name=course_names, course=course_ids, file=file_names, host=host)
