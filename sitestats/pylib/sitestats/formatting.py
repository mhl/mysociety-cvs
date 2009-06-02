#
# formatting.py: Formatting functions for mySociety site statistics
# Copyright (c) 2009 UK Citizens Online Democracy. All rights reserved.
# Email: louise@mysociety.org; WWW: http://www.mysociety.org/
#
# $Id: formatting.py,v 1.1 2009-06-02 18:14:24 louise Exp $
#
import sitestats
from django.conf import settings
settings.configure( TEMPLATE_DIRS=(sitestats.package_dir + '/../../templates/',), TEMPLATE_DEBUG=True)
from django.template.loader import render_to_string

def format_cell_value(format, info):
    link = info.get('link')
    unit = info.get('unit', '')
    percent_change = info.get('percent_change')
    current_value = info.get('current_value')
    result = "%s%s" % (current_value, unit)
    if format == 'html':
        if link:
            result = "<a href='%s'>%s</a>" % (link, result)  
    if percent_change:
        result += " (%s)" % (percent_change)    
    return result

def render_table(format, headers, rows, totals):
    template_params = {}
    if format == 'html':
        file_ext = 'html'
    elif format == 'text':
        file_ext = 'txt'
        totals = ['Totals'] + totals
        table_data = [headers] + rows + [totals]
        pad_text_table(table_data)
        template_params['row_separator'] = text_table_row_separator(table_data, '-')
    template_params.update({'headers': headers, 'rows': rows, 'totals'  : totals})
    rendered = render_to_string('table.' + file_ext, template_params)
    return rendered
    
def text_table_row_separator(rows, char='-'):  
    width = max([table_row_char_size(row) for row in rows])
    head = ''
    for i in range(1, width):
        head += char
    return head

def pad_text_table(rows):
    for column_index in range(0, len(rows[0])):
        pad_column(rows, column_index, max_size(rows, column_index))

def pad_column(rows, column_index, width):
    for row in rows:
        row[column_index] = str(row[column_index]).ljust(width)
        
def max_size(rows, column_index):
    return max([len(str(row[column_index])) for row in rows])
    
def table_row_char_size(row):
    # assumes cells will be padded one char on each side
    return sum([len(str(cell_contents)) + 2 for cell_contents in row]) + len(row) 