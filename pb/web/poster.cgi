#!/usr/bin/env python2.3
#
# poster.cgi:
# Creates a poster for printing out
#
# Copyright (c) 2005 UK Citizens Online Democracy. All rights reserved.
# Email: matthew@mysociety.org; WWW: http://www.mysociety.org/
#
# $Id: poster.cgi,v 1.4 2005-03-04 15:07:31 matthew Exp $
#

import sys
import cgi
import cgitb; cgitb.enable()
from time import time
from pyPgSQL import PgSQL

#print "Content-Type: text/html\r\n\r\n"

sys.path.append("../../pylib")
import mysociety.config
mysociety.config.set_file("../conf/general")

db = PgSQL.connect('::pb:matthew:')

form = cgi.FieldStorage()
ref = form.getfirst("ref", "")
type = form.getfirst("type", "cards")
size = form.getfirst("size", "A4")

# print "Content-Type: text/html\r\n\r\n";
q = db.cursor()
q.execute('SELECT title, date FROM pledges WHERE ref = %s', ref)
(title,date) = q.fetchone()
q.close()
db.close()

from reportlab.pdfgen import canvas
from reportlab.lib.units import cm

outdir = mysociety.config.get("PB_PDF_CACHE")
outfile = "%s_%s.pdf" % (ref, type)

def draw_pledge(x, y):
    text = "\"%s\"" % title
    size = 14*10/(c.stringWidth(text, "Helvetica", 14)/cm)
    c.setFont("Helvetica", size)
    c.drawCentredString(x, (y-1)*cm, text)

    text = "Deadline: %s" % date
    size = 14*10/(c.stringWidth(text, "Helvetica", 14)/cm)
    c.setFont("Helvetica", size)
    c.drawCentredString(x, (y-2)*cm, text)

    text = "http://pledgebank.com/%s" % ref
    size = 14*10/(c.stringWidth(text, "Helvetica", 14)/cm)
    c.setFont("Helvetica", size)
    c.drawCentredString(x, (y-3)*cm, text)

def cards():
    #c.setStrokeColorRGB(0.5, 1, 0.5)
    #c.setFillColorRGB(0.61, 0.5, 0.72)
    c.setStrokeColorRGB(0,0,0)
    c.setFillColorRGB(0,0,0)
    # c.setLineWidth(1)
    c.setDash(3,3)
    c.line(10.5*cm, 0, 10.5*cm, 30*cm)
    for y in (5,10,15,20,25,30):
        c.line(0,y*cm,21*cm,y*cm)
        c.setFont("ZapfDingbats",24)
        c.drawString(1*cm, y*cm-8, '"')
        draw_pledge(10.5*cm/2, y)
        draw_pledge(10.5*cm*3/2, y)
    c.rotate(-90)
    c.setFont("ZapfDingbats",24)
    c.drawString(-29*cm, 10.5*cm-8, '"')
    c.showPage()

# c.rotate(90)
#import reportlab.rl_config
#reportlab.rl_config.warnOnMissingFontGlyphs = 0
#from reportlab.pdfbase import pdfmetrics
#from reportlab.pdfbase.ttfonts import TTFont
#from reportlab.lib.fonts import addMapping
#pdfmetrics.registerFont(TTFont('Cyberbit', 'Cyberbit.ttf'))
#c.setFont('Cyberbit', 32)
#c.drawString(10, 15*cm, "\xc3\xa9Some text encoded in UTF-8")
#c.drawString(10, 10*cm, "In the Cyberbit TT Font!")

def tearoff():
    x = 10.5*cm
    y = 20
    text = "\"%s\"" % title
    size = 32/(c.stringWidth(text, "Helvetica", 32)/cm)*19
    c.setFont("Helvetica", size)
    c.drawCentredString(x, (y-1)*cm, text)
    c.setFont("Helvetica", size*0.8)
    text = "Deadline: %s" % date
    c.drawCentredString(x, (y-3)*cm, text)
    text = "http://pledgebank.com/%s" % ref
    c.drawCentredString(x, (y-5)*cm, text)
    c.setDash(3,3)
    stripheight = 8*cm
    c.line(0, stripheight, 21*cm, stripheight)
    c.rotate(90)
    for x in (3, 6, 9, 12, 15, 18, 21):
        c.line(0, -x*cm, stripheight, -x*cm)
        c.setFont("ZapfDingbats", 24)
        c.drawString(1*cm, -x*cm-9, '"')
        c.setFont("Helvetica", 10)
        text = "\"%s\"" % title
        c.drawCentredString(stripheight/2, (2.2-x)*cm, text)
        c.setFont("Helvetica", 9)
        text = "Deadline: %s" % date
        c.drawCentredString(stripheight/2, (1.2-x)*cm, text)
        text = "http://pledgebank.com/%s" % ref
        c.drawCentredString(stripheight/2, (0.7-x)*cm, text)
    c.showPage()

#c.rotate(-90)
#c.setFont('Courier', 12)
#t = c.beginText(10, 29*cm)
#t.textOut("test ")
#t.setRise(6)
#t.textOut("more test\nIndeed")
#t.setRise(0)
#t.textOut("and some more")
#c.drawText(t)

c = canvas.Canvas(outdir + '/' + outfile)
if type == "cards":
    cards()
elif type == "tearoff":
    tearoff()
else:
    raise Exception, "Unknown type '%s'" % type
c.save()

print "Location: %s/%s" % (mysociety.config.get('PB_PDF_URL'), outfile)
print
print "<h1>301 Found</h1>"

#print "Content-Type: text/html\r\n\r\n"
#print mysociety.config.get("BASE_URL")
