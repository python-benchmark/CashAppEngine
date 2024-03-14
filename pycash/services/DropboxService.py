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

from django.conf import settings
from dropbox import client, rest, session
from dropbox.session import OAuthToken
from pycash.services.Utils import get_logger
from pycash.models import StoredToken

APP_KEY = getattr(settings,'DROPBOX_APPKEY','')
APP_SECRET = getattr(settings,'DROPBOX_APPSECRET','')
ACCESS_TYPE = getattr(settings,'DROPBOX_ACCESTYPE','app_folder')  # should be 'dropbox' or 'app_folder'

class StorageService():
    
    def __init__(self):
        self.sess = StoredSession(APP_KEY, APP_SECRET, access_type=ACCESS_TYPE)
        self.api_client = client.DropboxClient(self.sess)
        self.current_path = ''
        self.sess.load_creds()
        
    def do_login(self):
        """log in to a Dropbox account"""
        try:
            self.sess.link()
        except rest.ErrorResponse, e:
            get_logger().error(str(e))
            raise
        
    def do_logout(self):
        """log out of the current Dropbox account"""
        self.sess.unlink()
        self.current_path = ''            

    def file_delete(self, path):
        """delete a file or directory"""
        self.api_client.file_delete(self.current_path + "/" + path)
        
    def file_rename(self, from_path, to_path):
        """move/rename a file or directory"""
        self.api_client.file_move(self.current_path + "/" + from_path,
                                  self.current_path + "/" + to_path)
        
    def file_put(self, from_file, to_path):
        """
        Copy local file to Dropbox
        """
        self.api_client.put_file(self.current_path + "/" + to_path, from_file)
        
    def do_get(self, from_path, dest_file):
        """
        Copy file from Dropbox to local.
        """
        f, metadata = self.api_client.get_file_and_metadata(self.current_path + "/" + from_path)
        dest_file.write(f.read())
        
class StoredSession(session.DropboxSession):
    """a wrapper around DropboxSession that stores a token to db"""

    def load_creds(self):
        try:
            sttoken = StoredToken.objects.get(token_key=self.consumer_creds.key, token_secret=self.consumer_creds.secret)
            stored_creds = sttoken.token
            self.set_token(*stored_creds.split('|'))
        except StoredToken.DoesNotExist:
            pass

    def write_creds(self, token):
        try:
            sttoken = StoredToken.objects.get(token_key=self.consumer_creds.key, token_secret=self.consumer_creds.secret)
        except StoredToken.DoesNotExist:
            sttoken = StoredToken(token_key=self.consumer_creds.key, token_secret=self.consumer_creds.secret)
        sttoken.token = "|".join([token.key, token.secret])
        sttoken.save()

    def delete_creds(self):
        try:
            sttoken = StoredToken.objects.get(token_key=self.consumer_creds.key, token_secret=self.consumer_creds.secret)
            sttoken.delete()
        except StoredToken.DoesNotExist:
            pass

    def get_access_token(self, request_token = None):
        if not request_token:
            request_token = self.obtain_request_token()
            url = self.build_authorize_url(request_token)
            return url, request_token
        return self.obtain_access_token(request_token)
                
    def link(self):
        self.write_creds(self.token)

    def unlink(self):
        self.delete_creds()
        session.DropboxSession.unlink(self)