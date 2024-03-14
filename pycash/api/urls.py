from django.conf.urls.defaults import patterns, url

urlpatterns = patterns('pycash.api.views',
    url(r'^import/$', 'import_data', name="import"),
)
