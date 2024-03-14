from django.conf.urls.defaults import patterns, url, include

urlpatterns = patterns('',
    (r'^mobile/',include('pycash.controllers.url.mobile', namespace='mobile')),
    (r'^paymentType/',include('pycash.controllers.url.paymentType')),
    (r'^subCategory/',include('pycash.controllers.url.subCategory')),
    (r'^tax/',include('pycash.controllers.url.tax')),
    (r'^loan/',include('pycash.controllers.url.loan')),
    (r'^payment/',include('pycash.controllers.url.payment')),
    (r'^income/',include('pycash.controllers.url.income')),
    (r'^expense/',include('pycash.controllers.url.expense')),
    (r'^stats/',include('pycash.controllers.url.stats')),
    (r'^category/',include('pycash.controllers.url.category')),
    (r'^person/',include('pycash.controllers.url.person')),
    (r'^card/',include('pycash.controllers.url.card')),                       
    (r'^cardDates/',include('pycash.controllers.url.cardDates')),
    (r'^cardExpense/',include('pycash.controllers.url.cardExpense')),
    (r'^debits/',include('pycash.controllers.url.debits')),
    (r'^sync/',include('pycash.controllers.url.sync')),
    (r'^token/',include('pycash.controllers.url.token', namespace='token')),
)
