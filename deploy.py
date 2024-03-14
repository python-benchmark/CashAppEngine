#!/usr/bin/python

import sys, os

sys.path.append(os.path.abspath(os.path.dirname(__file__)))

import StringIO
import settings
import optparse
import re

def update_version():
    input = open('app.yaml','rb')
    out = StringIO.StringIO()
    repl = re.compile('[^a-z\d\-]')
    for line in input:
        if line.startswith('version'):
            out.write('version: %s\n' % repl.sub('', settings.VERSION))
        else:
            out.write(line)
    input.close()
    fileout = open('app.yaml','wb')
    fileout.write(out.getvalue())
    fileout.close()
    out.close()

def prompt_continue():
    if getattr(settings,'APP_ID',False):
        s = "Deploy version %s on %s?" % (settings.VERSION, settings.APP_ID)
    else:    
        s = "Deploy version %s on default app?" % settings.VERSION
    
    r = raw_input(s + " (Y/n): ")
    return not r or r == '' or r.lower() == 'y'
    
def main():
    update_version()
    if prompt_continue():
        cmd = 'appcfg.py'
        if getattr(settings,'APP_ID',False):
            cmd += ' -A %s' % settings.APP_ID
        if getattr(settings, 'APP_USER',False):
            cmd += ' --email=%s' % settings.APP_USER
        if getattr(settings,'APP_TOKEN', False):
            cmd += ' --oauth2_refresh_token=%s' % settings.APP_TOKEN
        else:
            cmd += ' --oauth2 --noauth_local_webserver'
        cmd += ' update .'
        print cmd
        os.system(cmd)
        
if __name__ == '__main__':
    main()
