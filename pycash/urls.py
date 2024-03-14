from django.conf.urls.defaults import patterns, url, include
from django.conf import settings
from django.contrib import admin
from adminplus import AdminSitePlus
#from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.contrib.auth import views as auth_views

admin.site = AdminSitePlus()
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^admin/', include(admin.site.urls)),
    url(r'^login/$', 'pycash.views.login', name='user_signin'),
    url(r'^logout/$', auth_views.logout, {'next_page': settings.LOGOUT_REDIRECT_URL }, name='auth_logout'),
    url(r'^api/',include('pycash.api.urls', namespace='api')),
    url(r'^cron/',include('pycash.cron.urls', namespace='cron')),
    url(r'^$','pycash.views.mobile', name='home'),
    url(r'',include('pycash.controllers.urls')),
)

#urlpatterns += staticfiles_urlpatterns()
