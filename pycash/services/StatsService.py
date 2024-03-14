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
from pycash.services import DateService
from pycash.models import Expense, Income, StatsData, CategoryStatsData
from django.conf import settings
from pycash.services.Utils import logger

def generate_current():
    date = DateService.todayDate() 
    fromDate = DateService.firstDateOfMonth(date)
    toDate = DateService.lastDateOfMonth(date)
    create_stats(fromDate, toDate)
    
def generate():
    date = DateService.addMonth(DateService.todayDate(),-1) 
    fromDate = DateService.addMonth(DateService.firstDateOfMonth(date),-6)
    toDate = DateService.lastDateOfMonth(date)
    
    values = DateService.getMonthRange(fromDate, toDate)

    for value in values:
        create_stats(*value)
    
def create_category_stats(fromDate, toDate):
    logger.debug("Process Categories %s - %s" % (fromDate, toDate))
    month = fromDate.strftime('%Y%m')
    
    categoryCache = {}
    
    categoryExclude = getattr(settings, 'STATS_CATEGORY_EXCLUDE', [])
    subCategoryExclude = getattr(settings, 'STATS_SUBCATEGORY_EXCLUDE', [])
    
    q = Expense.objects.filter(date__gte=fromDate, date__lte=toDate)
    for expense in q:
        if not (expense.subCategory.pk in subCategoryExclude or expense.subCategory.category.pk in categoryExclude):
            category = categoryCache.get(expense.subCategory.category.pk)
            if not category:
                category = {'category': expense.subCategory.category, 'amount': 0}
            category['amount'] += expense.amount
            categoryCache[expense.subCategory.category.pk] = category

    CategoryStatsData.objects.filter(month=month).delete()
    
    for c in categoryCache.values():
        if c['amount'] > 0:
            CategoryStatsData.objects.create(month=month, category=c['category'], amount=c['amount'])
    
def create_stats(fromDate, toDate):
    logger.debug("Process %s - %s" % (fromDate, toDate))
    month = fromDate.strftime('%Y%m')
    
    incomeSum = 0
    for income in Income.objects.filter(period__gte=fromDate, period__lte=toDate):
        incomeSum += income.amount
    
    try:
        data = StatsData.objects.get(pk=month)
    except StatsData.DoesNotExist:
        data = StatsData(month=month)
        
    data.incomes = incomeSum
    
    expenseSum = 0
    
    q = Expense.objects.filter(date__gte=fromDate, date__lte=toDate)

    defaultpt = getattr(settings,'STATS_PAYMENT_TYPE', None)
    if defaultpt:
        q = q.filter(paymentType__id=defaultpt)

    categoryExclude = getattr(settings, 'MONTH_STATS_CATEGORY_EXCLUDE', [])
    subCategoryExclude = getattr(settings, 'MONTH_STATS_SUBCATEGORY_EXCLUDE', [])
                    
    for expense in q:
        if not (expense.subCategory.pk in subCategoryExclude or expense.subCategory.category.pk in categoryExclude):
            expenseSum += expense.amount
    
    data.expenses = expenseSum
    
    data.save()
    
    create_category_stats(fromDate, toDate)
    
def create_chart():
    import pygal
    #chart = pygal.Line()
    chart = pygal.Bar(disable_xml_declaration=True)
    chart.title = 'Gastos'
    
    q = StatsData.objects.all().order_by('-month')[:6]
    data = sorted(q, key=lambda d: d.month)
    
    labels = []
    expenses = []
    incomes = []
    for d in data:
        labels.append(d.display_month)
        expenses.append(float(d.expenses))
        incomes.append(float(d.incomes))
    
    chart.x_labels = labels   
    logger.debug(labels) 
    chart.add('Gastos', expenses)
    chart.add('Ingresos', incomes)
    
    return chart.render()

def create_category_chart(month):
    import pygal
    chart = pygal.Pie(truncate_legend=50, disable_xml_declaration=True)
    
#    date = DateService.todayDate()
#    month = date.strftime('%Y%m')
    
    q = CategoryStatsData.objects.filter(month=month)
    if q:
        chart.title = 'Gastos mes %s' % q[0].display_month
    
    for d in q:
        chart.add("%s [$%0.2f]" % (d.category.name, d.amount), float(d.amount))

    return (chart.render(), q)
