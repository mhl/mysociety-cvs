#!/usr/bin/env python2.5
#
# page.py:
# Front end shared functions
#
# Copyright (c) 2009 UK Citizens Online Democracy. All rights reserved.
# Email: matthew@mysociety.org; WWW: http://www.mysociety.org/
#
# $Id: page.py,v 1.5 2009-04-01 15:33:05 matthew Exp $
#

import os, re, cgi, fcgi

def fcgi_loop(main):
    req = fcgi.Accept()
    fs = req.getFieldStorage()

    try:
        response = main(fs)
        if response.headers():
            req.out.write(response.headers())

        req.out.write("Content-Type: text/html; charset=utf-8\r\n\r\n")
        if req.env.get('REQUEST_METHOD') == 'HEAD':
            req.Finish()
            return

        footer = template('footer')
        header = template('header', {
            'postcode': fs.getfirst('pc', ''),
            'refresh': response.refresh and '<meta http-equiv="refresh" content="%d">' % response.refresh or '',
            'body_id': response.id and ' id="%s"' % response.id or '',
        })
        req.out.write(header + str(response) + footer)

    except Exception, e:
        req.out.write("Content-Type: text/plain\r\n\r\n")
        req.out.write("Sorry, we've had some sort of problem.\n\n")
        req.out.write(str(e) + "\n")
        traceback.print_exc()

    req.Finish()

class Response(object):
    def __init__(self, template='', vars={}, status=200, url='', refresh=False, id=''):
        self.template = template
        self.vars = vars
        self.status = status
        self.url = url
        self.refresh = refresh
        self.id = id

    def __str__(self):
        if self.status == 302:
            return "Please visit <a href='%s'>%s</a>." % (self.url, self.url)
        return template(self.template, self.vars)

    def headers(self):
        if self.status == 302:
            return "Status: 302 Found\r\nLocation: %s\r\n" % self.url
        return ''

def pluralize(m, vars):
    if m.group('lookup'):
        n = vars.get(m.group('var'), []).get(m.group('lookup'), 0)
    else:
        n = vars.get(m.group('var'), 0)
    singular = m.group('singular') or ''
    plural = m.group('plural') or 's'
    if n==1:
        return singular
    return plural

def template(name, vars={}):
    template = slurp_file('../templates/%s.html' % name)
    vars['self'] = os.environ.get('REQUEST_URI', '')
    template = re.sub('{{ ([a-z_]*) }}', lambda x: cgi.escape(str(vars.get(x.group(1), '')), True), template)
    template = re.sub('{{ ([a-z_]*)\.([a-z_]*) }}', lambda x: cgi.escape(str(vars.get(x.group(1), []).get(x.group(2), '')), True), template)
    template = re.sub('{{ ([a-z_]*)\|safe }}', lambda x: str(vars.get(x.group(1), '')), template)
    template = re.sub('{{ (?P<var>[a-z_]*)(?:\.(?P<lookup>[a-z_]*))?\|pluralize(?::"(?P<singular>[^,]*),(?P<plural>[^"]*)")? }}',
        lambda x: pluralize(x, vars), template)
    return template

def slurp_file(filename):
    f = file(filename, 'rb')
    content = f.read()
    f.close()
    return content

def validate_email(address):
    if re.match('([^()<>@,;:\\".\[\] \000-\037\177\200-\377]+(\s*\.\s*[^()<>@,;:\\".\[\] \000-\037\177\200-\377]+)*|"([^"\\\r\n\200-\377]|\.)*")\s*@\s*[A-Za-z0-9][A-Za-z0-9-]*(\s*\.\s*[A-Za-z0-9][A-Za-z0-9-]*)*$', address):
        return True
    else:
        return False

