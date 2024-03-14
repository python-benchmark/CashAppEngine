from django.conf.urls.defaults import patterns, url, include
from pycash.controllers import PersonController as controller

urlpatterns = patterns('',
    url(r'^list$', controller.list),
    url(r'^save$', controller.save, name="person_save"),
    url(r'^update$', controller.update),
    url(r'^delete$', controller.delete),
)
