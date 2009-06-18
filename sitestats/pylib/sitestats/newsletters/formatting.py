#
# formatting.py: Formatting functions for mySociety site statistics
# Copyright (c) 2009 UK Citizens Online Democracy. All rights reserved.
# Email: louise@mysociety.org; WWW: http://www.mysociety.org/
#
# $Id: formatting.py,v 1.4 2009-06-18 09:14:11 louise Exp $
#
from django.template.loader import render_to_string

def format_cell_value(format, info):
    if not isinstance(info, dict):
        return info
    link = info.get('link')
    unit = info.get('unit', '')
    percent_change = info.get('percent_change')
    current_value = info.get('current_value')
    previous_value = info.get('previous_value')
    result = ''
    if current_value != None:
        result = "%s%s" % (current_value, unit)
        if format == 'html':
            if link:
                result = "<a href='%s'>%s</a>" % (link, result)  
        if percent_change:
            result += " (%s)" % (percent_change)    
    elif previous_value != None and percent_change != None:
        result = percent_change
        result += " (from %s%s)" % (previous_value, unit)
        if format == 'html':
            if link:
                result = "<a href='%s'>%s</a>" % (link, result)  
    else:
        raise str(info)
    return result

def render_table(format, headers, rows, totals=None):
    formatted_rows = []
    for row in rows: 
        formatted_row = [ format_cell_value(format, cell) for cell in row ]
        formatted_rows.append(formatted_row)
    template_params = {}
    if format == 'html':
        file_ext = 'html'
    elif format == 'text':
        file_ext = 'txt'
        if totals:
            totals = ['Totals'] + totals
            table_data = [headers] + formatted_rows + [totals]
        else:
            table_data = [headers] + formatted_rows
        pad_text_table(table_data)
        template_params['row_separator'] = text_table_row_separator(table_data, '-')
    template_params.update({'headers': headers, 'rows': formatted_rows, 'totals'  : totals})
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