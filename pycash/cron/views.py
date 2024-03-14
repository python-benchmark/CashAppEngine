# -*- coding: utf-8 -*-
"""Copyright (c) 2012 Sergio Gabriel Teves
All rights reserved.

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.

"""
from django.core import serializers
from pycash.decorators import json_response
from pycash.models import SyncRecord, Expense
from pycash.services.DropboxService import StorageService
from pycash.services import DateService, StatsService
import datetime
import StringIO
import gzip
from pycash.services import RequestUtils
from pycash.services.Utils import logger
from django.core.mail import mail_managers as send_mail
from django.utils.encoding import smart_str

@json_response
def backup(request):
    if RequestUtils.param_exist("date", request.REQUEST):
        today = datetime.datetime.strptime(request.REQUEST['date'],"%Y%m%d")
    else:
        today = datetime.date.today()
    fromDate = DateService.midNight(today - datetime.timedelta(days=7))
    toDate = DateService.midNight(today)
    try:
        records = SyncRecord.objects.filter(created__gte=fromDate, created__lt=toDate)
        data = serializers.serialize("xml", records);
        filename = "%s_cashbackup.xml" % today.strftime("%Y%m%d")
        filedata = StringIO.StringIO()
        zipped = gzip.GzipFile(filename, 'wb', fileobj=filedata)
        zipped.write(data)
        zipped.close()
        st = StorageService()
        st.file_put(filedata.getvalue(), filename + ".gz")
        error = ''
    except Exception, e:
        logger.error(str(e))
        send_mail("EXPORT ERROR", 'Processing %s.\n\nError: %s' % (today.strftime("%Y-%m-%d"), str(e)))
        error=str(e)
    return {'processed': today.strftime("%Y-%m-%d"), 'sync': records.count(), 'error': error}

@json_response
def updateevent(request):
    from pycash.management.commands.updateevent import Command
    response = StringIO.StringIO()
    cmd = Command()
    cmd.stdout = response
    cmd.handle()
    return {'process': response.getvalue()}
    
@json_response
def generatestats(request):
    StatsService.generate()
    return {'process': 'ok'}
    
@json_response
def generatemonthstats(request):
    StatsService.generate_current()
    return {'process': 'ok'}    
    
@json_response
def report(request):
    if RequestUtils.param_exist("date", request.REQUEST):
        date = DateService.parseDate(request.REQUEST['date'])
    else:
        date = DateService.addMonth(DateService.todayDate(),-1)
    fromDate = DateService.midNight(DateService.firstDateOfMonth(date))
    toDate = DateService.midNight(DateService.lastDateOfMonth(date),True)
    try:
        q = Expense.objects.filter(date__gte=fromDate, date__lte=toDate)
        filedata = StringIO.StringIO()
        filedata.write('"pk","date","text","amount","paymentTypePk","paymentTypeName","categoryPk","categoryName","subCategoryPk","subCategoryName"\n')
        for expense in q:
            d = {'pk': expense.pk,
                'date': DateService.invert(expense.date),
                'text': expense.text,
                'amount': expense.amount,
                'paymentTypePk': expense.paymentType.pk,
                'paymentTypeName': expense.paymentType.name,
                'categoryPk': expense.subCategory.category.pk,
                'categoryName': expense.subCategory.category.name,
                'subCategoryPk': expense.subCategory.pk,
                'subCategoryName': expense.subCategory.name}
            filedata.write(smart_str('%(pk)s,%(date)s,"%(text)s",%(amount)s,%(paymentTypePk)s,"%(paymentTypeName)s",%(categoryPk)s,"%(categoryName)s",%(subCategoryPk)s,"%(subCategoryName)s"\n' % d, 'latin1'))
        
        filename = "expensereport_%s.csv" % fromDate.strftime("%Y%m")
        
        if RequestUtils.param_exist("gz", request.REQUEST):
            filezip = StringIO.StringIO()
            zipped = gzip.GzipFile(filename, 'wb', fileobj=filezip)
            zipped.write(filedata)
            zipped.close()
            st = StorageService()
            st.file_put(filezip.getvalue(), filename + ".gz")
        else:
            st = StorageService()
            st.file_put(filedata.getvalue(), filename)
        error = ''
    except Exception, e:
        logger.error(str(e))
        send_mail("EXPORT ERROR", 'Processing %s.\n\nError: %s' % (fromDate.strftime("%Y-%m"), str(e)))
        error=str(e)
    return {'processed': fromDate.strftime("%Y-%m"), 'error': error}
    
    
