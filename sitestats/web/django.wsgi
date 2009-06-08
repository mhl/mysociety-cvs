import os
import sys
filename = __file__
file_dir = os.path.abspath(os.path.realpath(os.path.dirname(filename)))
sys.path.append(file_dir+"/../pylib")
os.environ['DJANGO_SETTINGS_MODULE'] = 'sitestats.settings'

import django.core.handlers.wsgi
application = django.core.handlers.wsgi.WSGIHandler()
