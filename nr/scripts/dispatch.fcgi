#!/home/am/amvoliman.com/private-python/bin/python

import site
site.addsitedir('/home/am/amvoliman.com/av4live/lib/python2.6/site-packages/')

import sys
import os

#sys.path.insert('/home/am/amvoliman.com/projects/av4repo/av4')

sys.path.append('/home/am/amvoliman.com/projects/av4repo/av4')

os.environ['DJANGO_SETTINGS_MODULE'] = 'av4.settings.production'

from django.core.servers.fastcgi import runfastcgi
runfastcgi(method="threaded", daemonize="false")

