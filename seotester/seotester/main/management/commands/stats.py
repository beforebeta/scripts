from django.core.management import BaseCommand
from seotester import print_stack_trace
from seotester.main.models import Crawl, URLManager


class Command(BaseCommand):

    def handle(self, *args, **options):
        try:
            print "Crawl Stats"
            for c in Crawl.objects.all():
                c.generate_stats()
            print "URL Stats"
            URLManager().generate_stats()
            print "Done"
        except:
            print_stack_trace()