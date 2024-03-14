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
from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.template import RequestContext
from django.contrib.auth import views as auth_views
from django import forms
from django.utils.translation import ugettext as _
from common.decorators import superuser_required
from common.view.decorators import render
from pycash.models import StoredToken

@login_required
def index(request):
    if request.is_mobile:
        return mobile(request)
    return render_to_response('cash/index.html', context_instance=RequestContext(request))

@login_required
def mobile(request):
    return render_to_response('mobile/index.html', context_instance=RequestContext(request))
    
def login(request, template_name='login.html'):
    if request.method == 'POST':
        if not request.POST.get('remember', None):
            request.session.set_expiry(0)
    if True or request.is_mobile:
        template_name="mobile/login.html"
    return auth_views.login(request, template_name)

@superuser_required
@render('admin/tokens.html')
def storeauthsetup(request):
    requrl = None
    reqid = None
    if request.method == 'POST':
        from pycash.services.DropboxService import StorageService, OAuthToken
        stService = StorageService()
        session = stService.sess
        if request.POST.get('reqid', None):
            token = request.POST.get('reqid').split('|')
            session.get_access_token(OAuthToken(*token))
            session.link()
        else:
            requrl, token = session.get_access_token()
            reqid = "|".join([token.key, token.secret])
    elif request.GET.get('delete', None):
        try:
            s = StoredToken.objects.get(pk=request.GET.get('delete'))
            s.delete()
        except:
            pass
    tokens = StoredToken.objects.all()
    return {'tokens': tokens, 'reqid': reqid, 'requrl': requrl}

class StoredTokenForm(forms.Form):
    token_key = forms.CharField(label=_('App Key'))
    token_secret = forms.CharField(label=_('App Secret'))