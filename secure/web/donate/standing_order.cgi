#!/usr/bin/env python2.3
#
# standing_order.cgi:
# Creates standing order mandates for printing out.
#
# Run from the command line to test files.
#
# Copyright (c) 2006 UK Citizens Online Democracy. All rights reserved.
# Email: louise@mysociety.org; WWW: http://www.mysociety.org/
#
# $Id: standing_order.cgi,v 1.2 2007-09-06 17:11:29 matthew Exp $
#


############################################################################
import sys
sys.path.append("../../../pylib")

import fcgi
import gettext
import tempfile
import os
import string
from pyPgSQL import PgSQL

import mysociety.config
mysociety.config.set_file("../../conf/general")


from reportlab.pdfgen import canvas
from reportlab.lib.units import cm
from reportlab.lib.pagesizes import A4, LETTER # only goes down to A6
from reportlab.lib.units import cm
from reportlab.platypus import Paragraph, Frame
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_RIGHT

# font handling
from reportlab.pdfbase import pdfmetrics, ttfonts
from reportlab.pdfbase.pdfmetrics import _fonts
from reportlab.lib.fonts import addMapping

_ = gettext.gettext

db = PgSQL.connect(mysociety.config.get('DONATIONS_DB_HOST') + ':' + mysociety.config.get('DONATIONS_DB_PORT') + ':' + mysociety.config.get('DONATIONS_DB_NAME') + ':' + mysociety.config.get('DONATIONS_DB_USER') + ':' + mysociety.config.get('DONATIONS_DB_PASS'))

#--------------------------------------------------------------------------
def one_field_line(c, textobject, field, y, page_settings):
    """
    Prints a line with one prompt text and an underline to the end of the
    page. Moves the cursor one line down.
    """
    textobject.setTextOrigin(page_settings['margin_left'], y)
    textobject.textOut("%s: " % field )
    x = textobject.getX()
    c.line(x, y, page_settings['end_of_line'], y)
    return y - page_settings['line_spacing']

#--------------------------------------------------------------------------
def two_field_line(c, textobject, left_field, right_field, divider, y, page_settings):
    """
    Prints a line with two prompt texts followed by underlines to the end of the
    page. Moves the cursor one line down.
    """

    divide_point = page_settings['margin_left']                 \
                   + ((page_settings['end_of_line']             \
                   - page_settings['margin_left']) * divider) 
    textobject.setTextOrigin(page_settings['margin_left'], y)
    textobject.textOut("%s: " % left_field )
    x = textobject.getX()
    c.line(x,  y , divide_point, y)
    textobject.setTextOrigin(divide_point + 5, y)
    textobject.textOut("%s: " % right_field)
    x = textobject.getX()
    c.line(x,  y , page_settings['end_of_line'], y)
    return y - page_settings['line_spacing']

#--------------------------------------------------------------------------
def text_line(c, textobject, text, y, page_settings):
    """ 
    Prints a line of text, moves the cursor one line down 
    """
    textobject.setTextOrigin(page_settings['margin_left'], y)
    textobject.textOut("%s " % text )
    return y - page_settings['line_spacing']
#--------------------------------------------------------------------------
def standard_frame(height, bottom, page_settings):
    return Frame(page_settings['margin_left'], bottom, page_settings['frame_width'], 
        height, showBoundary = 0, leftPadding = 0, rightPadding = 0, topPadding = 5,
        bottomPadding = 5)
#--------------------------------------------------------------------------
def generate_pdf(c, ref):
    """
    Generates the pdf standing order mandate
    """

    (page_width, page_height) = A4
    (logo_width, logo_height) = (250, 49)
    margin_top = 2 * cm
    margin_left = 2 * cm
    margin_bottom = 2 * cm
    margin_right = 2 * cm
	
    small_writing = 12
    large_writing = 20
    line_spacing = 36

    frame_width = page_width - margin_left - margin_right
    frame_height = page_height - margin_top - margin_bottom
    end_of_line = page_width - margin_right

    page_settings = { 'margin_left': margin_left,
                      'end_of_line': end_of_line,
                      'line_spacing': line_spacing,
                      'frame_width': frame_width }

    c.setStrokeColorRGB(0,0,0)
    c.setFillColorRGB(0,0,0)

    # set up the fonts 
    heading_font = 'Helvetica'
    main_font = 'Helvetica'

    # set up the styles
    p_normal = ParagraphStyle('normal', alignment = TA_LEFT, spaceBefore = 12, spaceAfter = 12, 
        fontSize = small_writing, leading = small_writing*1.2, fontName = main_font)

    p_close = ParagraphStyle('normal', alignment = TA_LEFT, spaceBefore = 0, spaceAfter = 0,
        fontSize = small_writing, leading = small_writing*1.2, fontName = main_font)

    p_head = ParagraphStyle('normal', alignment = TA_LEFT, spaceBefore = 0, spaceAfter = 0, 
        fontSize = large_writing, leading = large_writing*1.2, fontName = heading_font)

    # mySociety logo 
    c.drawInlineImage("mysociety-dark.jpg", margin_left, frame_height, logo_width, logo_height)

    #generate the intro text
    text = [Paragraph(_("Thank you for supporting mySociety"), p_normal)]

    text.extend([Paragraph(_("""You opted to donate by monthly standing order.
                              Please fill in the form below and send it to: """), p_normal)])

    text.extend([Paragraph(_("""F.A.O. Tom Steinberg"""), p_close)])
    text.extend([Paragraph(_("""12 Duke's Road,"""), p_close)])
    text.extend([Paragraph(_("""London WC1H 9AD"""), p_close)])

    text.extend([Paragraph(_("""Thanks again for your support."""), p_normal)])
    text.extend([Paragraph(_("""Best wishes,"""), p_close)])

    text.extend([Paragraph(_("""Tom Steinberg, Director mySociety."""), p_normal)])

    # draw it to a frame    
    intro_frame_height = 7 * cm
    intro_text_bottom = page_height - margin_top - logo_height - intro_frame_height
   
    f = standard_frame(intro_frame_height, intro_text_bottom, page_settings)
    f.addFromList(text, c)

    # end with a line
    c.line(margin_left, intro_text_bottom, page_width - margin_right, intro_text_bottom)
    
    # standing order mandate
    text = [Paragraph(_("Standing Order Mandate:"), p_head)]

    text.extend([Paragraph(_("""UK Citizens Online Democracy 
                                registered charity number 1076346"""), p_normal)])

    text.extend([Paragraph(_("""To The Manager,"""), p_normal)])

    header_frame_height = 2 * cm
    header_frame_bottom =  intro_text_bottom - header_frame_height
    f = standard_frame(header_frame_height, header_frame_bottom, page_settings) 
    f.addFromList(text, c)
 
    textobject = c.beginText(margin_left, header_frame_bottom)
    textobject.setFont("Helvetica", 12)
    y = header_frame_bottom
 
    y = two_field_line(c, textobject, "Name of bank", "Sort code", 0.6, y, page_settings)
    y = one_field_line(c, textobject, "Branch", y, page_settings)
    y = one_field_line(c, textobject, "Branch Address", y, page_settings)
    
    c.line(margin_left, y, page_width - margin_right, y)
    
    y = y - (line_spacing / 2)

    payment_frame_height = 2 * cm
    payment_frame_bottom = y - payment_frame_height
    f = standard_frame(payment_frame_height, payment_frame_bottom, page_settings)

    text = [Paragraph(_("""Please pay HSBC Holborn Circus, 31 Holborn, London, EC1N 2HR
                           (for the credit of UK Citizens Online Democracy, sort code 
                           40-03-28, account number 31546341)"""), p_normal)]
   
    f.addFromList(text, c)
    y = payment_frame_bottom
    y = one_field_line(c, textobject, 'the sum of \243' , y, page_settings)
    y = one_field_line(c, textobject, "and in words", y, page_settings)
    y = two_field_line(c, textobject, "monthly on the" , "of each month, beginning", 0.4, y, page_settings)

    y = text_line(c, textobject, """until further notice in writing and debit my account accordingly.""", y, page_settings)
    y = text_line(c, textobject, """Please quote my reference number: %s """ % ref, y, page_settings)
    y = two_field_line(c, textobject, "Account number" , "Account name" , 0.5, y, page_settings)
    y = two_field_line(c, textobject, "Signature" , "Date" , 0.5, y, page_settings)

    c.drawText(textobject)
    c.showPage()

#==========================================================================
#
# Main loop

while fcgi.isFCGI():
    req = fcgi.Accept()
    fs = req.getFieldStorage()
#    req.err.write("got request in standing_order.cgi, path: %s\n" % req.env.get('PATH_INFO'))

    try:
        if req.env.get('PATH_INFO'):
            incgi = True
            path_info = req.env.get('PATH_INFO').split('_')
            if len(path_info)>0:
                ref = path_info[0][1:]
	else:        

            incgi = False

            from optparse import OptionParser
            parser = OptionParser()
            parser.set_usage("""
        ./standing_order.cgi REF [OPTIONS]

    Generates a standing order mandate to UKCOD in PDF format.  Designed
    to be run as a FastCGI script, but can be run on the command line for testing.
    REF is the reference number to be output on the mandate.  The output
    is sent to standard output if run as a CGI.""")
            (options, args) = parser.parse_args()
            if len(args) <> 1:
                parser.print_help()
                req.err.write("specify standing order ref\n")
                continue
            ref = args[0] 
         
	# check that this is a donor reference
        q = db.cursor()
        q.execute('SELECT id FROM donor WHERE id = %s', ref)
        row = q.fetchone()
        if not row:
            raise Exception, "Unknown ref '%s'" % ref
        q.close()


        # Header
        if incgi:
            req.out.write("Content-Type: application/pdf\r\n\r\n")
  
	def file_to_stdout(filename):
            f = file(filename, 'rb')
            content = f.read()
            f.close()
            req.out.write(content)

        outdir = mysociety.config.get("DONATIONS_PDF_CACHE")
	outfile = "%s.pdf" % ref

        # Generate PDF file
        (canvasfileh, canvasfilename) = tempfile.mkstemp(dir=outdir,prefix='tmp')
        c = canvas.Canvas(canvasfilename, pagesize=A4)
        try:
            generate_pdf(c, ref)
        except Exception, e:
            req.err.write(string.join(e.args,' '))
            c.setStrokeColorRGB(0,0,0)
            c.setFont("Helvetica", 15)
            c.drawCentredString(10.5*cm, 25*cm, str(e))
            
        c.save()
        os.rename(canvasfilename, outdir + '/' + outfile)
        os.chmod(outdir + '/' + outfile, 0644)
        if (incgi):
            file_to_stdout(outdir + '/' + outfile)
        
    except Exception, e:
        req.out.write("Content-Type: text/plain\r\n\r\n")
        req.out.write(_("Sorry, we weren't able to make your standing order mandate.\n\n").encode('utf-8'))
        req.out.write(str(e) + "\n")

    req.Finish()

