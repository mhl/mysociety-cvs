#!/usr/bin/python
import sys

# Added by Duncan 2009-11-07 to find the mysoc libraries.
sys.path.extend(['../pylib', '../../pylib'])
import mysociety.config
mysociety.config.set_file('../conf/general')

from django.core.management import execute_manager
try:
    import settings # Assumed to be in the same directory.
except ImportError:
    import sys
    sys.stderr.write("Error: Can't find the file 'settings.py' in the directory containing %r. It appears you've customized things.\nYou'll have to run django-admin.py, passing it your settings module.\n(If the file settings.py does indeed exist, it's causing an ImportError somehow.)\n" % __file__)
    sys.exit(1)


# The django testing normally needs a database
# Let's monkey patch it so it doesn't...
def do_nothing(*args, **kwargs):
    return

from django.db import connection
connection.creation.create_test_db = do_nothing
connection.creation.destroy_test_db = do_nothing


if __name__ == "__main__":
    execute_manager(settings)
