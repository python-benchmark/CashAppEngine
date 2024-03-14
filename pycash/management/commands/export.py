from django.core.management.base import BaseCommand, CommandError
from pycash.services.ExportService import ExportService
from optparse import make_option
from pycash.models import *
from django.conf import settings
import datetime

class Command(BaseCommand):
    help = 'Export Data'
    db = 'export'
    chunks = getattr(settings, 'EXPORT_CHUNK_SIZE',50)
    expense_filter = getattr(settings, 'EXPORT_EXPENSE_DATE','2012-09-01')
    
    option_list = BaseCommand.option_list + (
        make_option('--username', dest='username', default=None, help='Specifies authorized Username.'),
        make_option('--token', dest='token', default=None, help='Specifies authorized Token.'),
        make_option('--key', dest='tokenkey', default=None, help='Specifies authorized user Token Key.'),
    )
    
    def handle(self, *args, **options):
        username = options.get('username', None)
        token = options.get('token', None)
        tokenkey = options.get('tokenkey', None)
        if not username or not token or not tokenkey:
            raise CommandError("You must specifiy a value for --username, --token and --key")
        
        self.stdout.write("Exporting data ...\n")
        
        self.service = ExportService(username, token, tokenkey)

        try:
            self.stdout.write("Sending payment types ...")
            self.send(PaymentType.objects.using(self.db).all())
            self.stdout.write("Sending categories ...")
            self.send(Category.objects.using(self.db).all())            
            self.stdout.write("Sending sub categories ...")
            self.send(SubCategory.objects.using(self.db).all())
            self.stdout.write("Sending persons ...")
            self.send(Person.objects.using(self.db).all())
            self.stdout.write("Sending loans ...")
            self.send(Loan.objects.using(self.db).all())   
            self.stdout.write("Sending loan payments ...")
            self.send(Payment.objects.using(self.db).all())
            self.stdout.write("Sending taxes ...")
            self.send(Tax.objects.using(self.db).all())                
            self.stdout.write("Sending incomes ...")
            self.send(Income.objects.using(self.db).all())     
            self.stdout.write("Sending expenses ...")
            self.send(Expense.objects.using(self.db).filter(date__gte=datetime.datetime.strptime(self.expense_filter,'%Y-%m-%d').date()))                              
        except Exception, e:
            self.stdout.write("Error: %s\n" % str(e))

    def send(self, data):
        c = 0
        if len(data) > self.chunks:
            self.stdout.write("\n")
            parts = (len(data) / self.chunks)+1
            p = 0
            for part in range(0,len(data),self.chunks):
                p +=1
                self.stdout.write("\tPart %d/%d ... " % (p, parts))
                r = self.do_send(data[part:part+self.chunks])
                if r == -1:
                    raise Exception() 
                c += r
        else:
            c = self.do_send(data)
            if c == -1:
                raise Exception()            
        self.stdout.write("Total sent %d. Confirmed %d.\n" % (len(data), c))
            
    def do_send(self, data):
        c = len(data)
        r = self.service.update(data)
        if r.status == 200:
            self.stdout.write(" loaded %s\n" % r.response['result'])
            rc = int(r.response['result'])
            assert c == rc, "Sent %d, confirmed %d" % (c,rc)
            return rc
        else:
            self.stdout.write(" error %s:%s\n" % (r.status, r.reason))
            return -1        
