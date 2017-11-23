from django.core.management.base import BaseCommand
from rippleAchievements.models import View, Task

class Command(BaseCommand):
    args = ''
    help = 'Populates the Views database'

    def handle(self, *args, **options):
        self.addView("add", "/questions/add", "addQuestion")
        self.addView("response", "/questions/response", "questionResponse")

    def addView(self, view, url, task):
        v = View(
            view=view,
            url=url
        ).save()
        t = Task(
            task=task
        ).save()
        t.views.add(v)
