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

from django.contrib import auth
from django.core.exceptions import ImproperlyConfigured
import logging

def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[-1].strip()
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip
    
class RemoteTokenMiddleware(object):
    """
    Middleware for utilizing Token based authentication.

    If request.user is not authenticated, then this middleware attempts to
    authenticate the username passed in the ``REMOTE_TOKEN`` request header.
    If authentication is successful, the user is automatically logged in to
    persist the user in the session.
    """

    token_header = "REMOTE_TOKEN"

    def process_request(self, request):
        # AuthenticationMiddleware is required so that request.user exists.
        if not hasattr(request, 'user'):
            raise ImproperlyConfigured(
                "The Django remote user auth middleware requires the"
                " authentication middleware to be installed.  Edit your"
                " MIDDLEWARE_CLASSES setting to insert"
                " 'django.contrib.auth.middleware.AuthenticationMiddleware'"
                " before the RemoteUserMiddleware class.")
        try:
            data = request.POST[self.token_header]
            username, token, token_key = data.split('-') 
        except:
            # If specified header doesn't exist then return (leaving
            # request.user set to AnonymousUser by the
            # AuthenticationMiddleware).
            return
        # If the user is already authenticated and that user is the user we are
        # getting passed in the headers, then the correct user is already
        # persisted in the session and we don't need to continue.
        
        # We are seeing this user for the first time in this session, attempt
        # to authenticate the user.
        try:
            user = auth.authenticate(remote_token=token, remote_user=username, remote_ip=get_client_ip(request), token_key=token_key)
            if user:
                request.user = user
                auth.login(request, user)
            else:
                # if passed data is invalid and there is an authenticated session,
                # we destroy the current logged session
                auth.logout(request)
        except:
            pass