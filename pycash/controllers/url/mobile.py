# -*- coding: utf-8 -*-
"""Copyright (c) 2011 Sergio Gabriel Teves
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
from django.conf.urls.defaults import patterns, url
  
urlpatterns = patterns('django.views.generic.simple',
    url(r'^expenses/$', 'direct_to_template', {'template': 'mobile/expenses.html'}, name='expenses'),
    url(r'^settings/$', 'direct_to_template', {'template': 'mobile/settings.html'}, name='settings'),
    url(r'^person/add/$', 'direct_to_template', {'template': 'mobile/person_add.html'}, name='person_add'),
    url(r'^income/add/$', 'direct_to_template', {'template': 'mobile/income_add.html'}, name='income_add'),
    url(r'^$', 'direct_to_template', {'template': 'mobile/index.html'}, name='home'),
)

urlpatterns += patterns('pycash.controllers.MobileController',
    url(r'^expenses/add/$', 'expensesAdd', name='expenses_add'),
    url(r'^expenses/edit/(?P<id>[\d]+)/$', 'expensesAdd', name='expenses_edit'),
    url(r'^expenses/list/$', 'expensesList', name='expenses_list'),
    url(r'^loans/$', 'loansHome', name='loans'),
    url(r'^loans/add/(?P<id>[\d]+)/$', 'loans_add', name='loans_add'),
    url(r'^loans/edit/(?P<id>[\d]+)/(?P<loanId>[\d]+)/$', 'loans_add', name='loans_edit'),
    url(r'^loans/list/(?P<id>[\d]+)/$', 'loans_list', name='loans_list'),
    url(r'^loans/list/(?P<id>[\d]+)/all/$', 'loans_list_all', name='loans_list_all'),
    url(r'^loans/payments/(?P<id>[\d]+)/$', 'loans_payments', name='loans_payments'),
    url(r'^loans/payments/(?P<id>[\d]+)/add/$', 'loans_payments_add', name='loans_payments_add'),
    url(r'^loans/payments/add/$', 'loans_payments_multi_add', name='loans_payments_multi_add'),
    url(r'^loans/payments/(?P<id>[\d]+)/edit/(?P<pId>[\d]+)/$', 'loans_payments_add', name='loans_payments_edit'),
    url(r'^tax/$', 'taxHome', name='tax'),
    url(r'^tax/list/$', 'taxList', name='tax_list'),
    url(r'^tax/add/$', 'taxAdd', name='tax_add'),
    url(r'^tax/edit/(?P<id>[\d]+)/$', 'taxAdd', name='tax_edit'),
    url(r'^tax/pay/(?P<id>[\d]+)/$', 'taxPay', name='tax_pay'),
    url(r'^income/list/$', 'incomeList', name='income_list'),
    url(r'^income/edit/(?P<id>[\d]+)/$', 'incomeEdit', name='income_edit'),
    url(r'^stats/$', 'stats', name='stats'),
    url(r'^statsCategory/$', 'stats_category', name='statsCategory'),
)