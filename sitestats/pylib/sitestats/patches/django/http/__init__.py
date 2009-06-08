import django.http
from django.conf import settings

def get_host(self):
    """Returns the HTTP host using the environment or request headers."""
    # We try three options, in order of decreasing preference.
    if settings.USE_X_FORWARDED_HOST and 'HTTP_X_FORWARDED_HOST' in self.META:
        host = self.META['HTTP_X_FORWARDED_HOST']
    elif 'HTTP_HOST' in self.META:
        host = self.META['HTTP_HOST']
    else:
        # Reconstruct the host using the algorithm from PEP 333.
        host = self.META['SERVER_NAME']
        server_port = str(self.META['SERVER_PORT'])
        if server_port != (self.is_secure() and '443' or '80'):
            host = '%s:%s' % (host, server_port)
    return host

django.http.HttpRequest.get_host = get_host
