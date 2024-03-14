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
from pycash.decorators import json_response
from django.core import serializers
from pycash.models import enable_sync, disable_sync
 
@json_response
def import_data(request):
    data = request.POST['data']
    c = 0
    # remove sync first
    disable_sync()
    for obj in serializers.deserialize("json",data):
        obj.save()
        c += 1
    enable_sync()
    return '{"success": true, "result": %d}' % c