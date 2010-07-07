import os
import sys

filename = __file__
file_dir = os.path.abspath(os.path.realpath(os.path.dirname(filename)))

path = file_dir + "/../pylib"
if path not in sys.path:
    sys.path.append(path)

os.environ['DJANGO_SETTINGS_MODULE'] = 'sitestats.settings'

import django.core.handlers.wsgi
application = django.core.handlers.wsgi.WSGIHandler()
