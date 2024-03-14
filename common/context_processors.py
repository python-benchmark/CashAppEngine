import time
import random

if hasattr(random, 'SystemRandom'):
    randrange = random.SystemRandom().randrange
else:
    randrange = random.randrange
    
def settings(request):
    from django.conf import settings
    return {'settings': settings}

def requestid(request):
    value = str(int(time.time()))[-4:]
    return {'requestid': str(randrange(9000, 9999)) + value}
    