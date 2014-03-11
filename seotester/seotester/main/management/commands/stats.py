from django.core.management import BaseCommand
from seotester.main.models import Crawl


class Command(BaseCommand):

    def handle(self, *args, **options):
        for c in Crawl.objects.all():
            c.generate_stats()

        print "done"