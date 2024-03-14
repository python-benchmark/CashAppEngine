from django.core.management.base import BaseCommand
from pycash.models import Tax
from django.conf import settings

class Command(BaseCommand):
    help = 'Update Events'

    def handle(self, *args, **options):
        if settings.USE_GOOGLE_CAL:
            from pycash.controllers.TaxController import update_calendar
            taxlist = Tax.objects.filter(updated=False)
            self.stdout.write("%d items to update.\n" % len(taxlist))
            a = 0
            for tax in taxlist:
                if update_calendar(tax.id):
                    a+=1
            self.stdout.write("%d items updated.\n" % a)
        else:
            self.stdout.write("Nothing to do.\n")