from django.conf.urls.defaults import patterns, url, include
from pycash.controllers import IncomeController as controller

urlpatterns = patterns('',
    (r'^stats$', controller.stats),                       
    (r'^list$', controller.list),
    url(r'^save$', controller.save_or_update, name="income_save"),
    url(r'^update$', controller.save_or_update, name="income_update"),
    url(r'^delete$', controller.delete, name="income_delete"),
    (r'^$', controller.index)
)

    

