import httplib, urllib
from urlparse import urlparse
from django.conf import settings
from django.core import serializers
from pycash.auth import generate_key
from django.utils import simplejson as json
import time

class ExportServiceResponse:
    status = 0
    reason = None
    response = None
    
class ExportService(object):

    def __init__(self, username, token, token_key):
        self.url = settings.EXPORT_URL
        self.username = username
        self.token = token
        self.token_key = token_key
        
    def update(self, data):
        rsp = ExportServiceResponse()
        try:
            postdata = serializers.serialize("json",data)
        except Exception, e:
            rsp.reason = str(e)
        else:            
            urldata = urlparse('//%s' % self.url)
            if time.localtime().tm_sec > 50:
                time.sleep(15)
            token_data = "%s-%s-%s"% (self.username, self.token, generate_key(self.token, self.token_key))
            params = urllib.urlencode({'REMOTE_TOKEN': token_data, 'data': postdata})
            conn = httplib.HTTPConnection(urldata.netloc, timeout=30)
            conn.request("POST", urldata.path, params)
            response = conn.getresponse()
            rsp.status = response.status
            rsp.reason = response.reason
            if response.status == 200:
                rsp.response = json.loads(response.read())
            conn.close()
        return rsp
