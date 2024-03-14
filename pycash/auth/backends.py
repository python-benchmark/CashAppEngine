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

from django.contrib.auth.backends import ModelBackend
from pycash.models import AuthToken, TokenUsage
from pycash.auth import generate_key
from django.conf import settings
from django.contrib.auth.models import User
import logging

class RemoteTokenBackend(ModelBackend):
    """
    This backend is to be used in conjunction with the ``RemoteTokenMiddleware``
    found in the middleware module of this package, and is used when the server
    is handling authentication outside of Django.
    """

    supports_anonymous_user = False
    supports_object_permissions = False
    
    def authenticate(self, remote_token, remote_user, remote_ip, token_key):
        
        if not remote_token or not remote_user:
            return

        user = None
        try:
            logging.debug("Token: %s User: %s IP: %s Key: %s" % (remote_token, remote_user, remote_ip, token_key))
            #Appengine legacy query
            user = User.objects.get(username=remote_user)
            authtoken = AuthToken.objects.get(token=remote_token, user=user)
            key = generate_key(authtoken.token, authtoken.token_key)
            logging.debug("GenKey: %s" % key)
            if not key == token_key:
                return None
            user = authtoken.user

            obj, created = TokenUsage.objects.get_or_create(token=authtoken, ip=remote_ip)
            if not created:
                obj.save() # if the object already exists, we force a save to update the last access date
        except (AuthToken.DoesNotExist, User.DoesNotExist):
            logging.DEBUG("NOT FOUND")
        return user

class SettingsAuthBackend:
    
    supports_anonymous_user = False
    supports_object_permissions = False
    
    def authenticate(self, username=None, password=None):
        if (username == getattr(settings,'ADMIN_LOGIN','admin') 
            and password ==  getattr(settings,'ADMIN_PWD','admin')):
            try:
                user = User.objects.get(username=username)
            except User.DoesNotExist:
                user = User.objects.create(username=username,
                                           is_staff=True,
                                           is_superuser=True)
            return user
        return None

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None
        
    def has_perm(self, user_obj, perm):
        return (user_obj==getattr(settings,'ADMIN_LOGIN','admin'))
