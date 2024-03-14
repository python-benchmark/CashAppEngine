from django.conf.urls.defaults import patterns, url, include
from pycash.controllers import SubCategoryController as controller

urlpatterns = patterns('',
    url(r'^list$', controller.list, name="subcategory_list"),
    (r'^save$', controller.save),
    (r'^update$', controller.update),
    (r'^delete$', controller.delete),
)
