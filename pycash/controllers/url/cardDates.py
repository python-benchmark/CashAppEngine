from django.conf.urls.defaults import patterns, url, include
from pycash.controllers import CardDatesController as controller

urlpatterns = patterns('',
    (r'^list$', controller.list),
    (r'^save$', controller.save),
    (r'^update$', controller.update),
    (r'^delete$', controller.delete),
)
