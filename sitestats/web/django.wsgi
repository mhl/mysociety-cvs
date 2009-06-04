import os
import sys
import sys
sys.path.extend(("../pylib"))

os.environ['DJANGO_SETTINGS_MODULE'] = 'sitestats.settings'

import django.core.handlers.wsgi
application = django.core.handlers.wsgi.WSGIHandler()
