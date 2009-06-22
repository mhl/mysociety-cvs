from django.db import models
from sitestats.newsletters import common
from sitestats.newsletters.formatting import render_table
from django.template.loader import render_to_string
from sitestats.newsletters.common import *

class NewsletterException(Exception):
    def __init__(self, value):
        self.value = value
    
    def __str__(self):
        return repr(self.value)
        
class Newsletter(models.Model):
    
    class Meta:
        app_label = 'newsletters'
        
    name = models.CharField(max_length=255)
    subject = models.CharField(max_length=255)
    site_id = None

    def __unicode__(self):
        return self.name
    
    def render(self, format, sources, date=None):
        """Returns the text for a TWFY email in text/html"""
        self.set_site_id(sources)
        if not self.formats.get(format):
            if not self.data:
                self.generate_data(sources, date)
            self.formats[format] =  self.render_data(format)
        return self.formats[format]

    def generate_data(self, sources, date):
        self.generate_traffic_data(sources, date)

    def render_data(self, format):
     '''Default content for a newsletter - a table of site traffic stats'''
     traffic_table = self.render_traffic_data(format)
     template_params = {'traffic_table'                  : traffic_table, 
                        'piwik_previous_week_link'       : self.data['piwik_previous_week_link'],
                        'piwik_previous_four_weeks_link' : self.data['piwik_previous_four_weeks_link']
                        }
     file_ext = format_extension(format)
     rendered = render_to_string(self.template() + '.' + file_ext, template_params)
     return rendered
                
    def render_traffic_data(self, format):
        if format == 'text':
          self.data['traffic_rows'] = self.data['traffic_rows'][:-1]
        return render_table(format, self.data['traffic_headers'], self.data['traffic_rows'])

    def set_site_id(self, sources):
        sites = sources['piwik'].sites()
        for site in sites:
            if site['name'].lower() == self.site_name.lower():
                self.site_id = site['id']
        if not self.site_id:
            raise NewsletterException("Couldn't find %s in piwik sites list" % self.site_name)
            
    def generate_traffic_data(self, sources, date):
        stats = self.traffic_stats()
        rows = []

        headers = ['', 'This week', '% change on last week', 'last 4 weeks', '% change on last 4 weeks']
        for (header, stat, unit) in stats['piwik']: 
            row = [header]
            row += self.get_traffic_data(stat, sources, unit, date)
            rows.append(row)
        piwik = sources['piwik']
        previous_week_link = piwik.site_link(site_id=self.site_id, date=date)
        previous_four_weeks_link = piwik.site_link(site_id=self.site_id, date='previous4')
        link_row = ['Piwik link', 
                    {'current_value' : 'link', 
                     'link' : previous_week_link}, 
                    '', 
                    {'current_value' : 'link', 
                     'link' : previous_four_weeks_link},
                    '']
        rows.append(link_row)
        self.data['piwik_previous_week_link'] = previous_week_link
        self.data['piwik_previous_four_weeks_link'] = previous_four_weeks_link
        self.data['traffic_headers'] = headers
        self.data['traffic_rows'] = rows

    def traffic_stats(self):
        """Returns a dictionary keyed by data source whose values are lists of tuples. Each tuple consists of the name of a
        statistic to be gathered, the method on the source class to use to get it and the units string to be used in displaying it."""

        stats =  {'piwik'  : [('Number of unique visitors', 'unique_visitors', ''), 
                              ('of this, number from UK Parliament', 'visitors_from_parliament', ''), 
                              ('Number of visits', 'visits', ''),
                              ('% from search', 'percent_visits_from_search', '%'),
                              ('% from other websites', 'percent_visits_from_sites', '%'),
                              ('% from direct access', 'percent_visits_from_direct_access', '%'),
                              ('% from UK Parliament', 'percent_visits_from_parliament', '%'),
                              ('Bounce rate (left after 1 page)', 'bounce_rate', '%'), 
                              ('page views/visit', 'pageviews_per_visit', ''),
                              ('time/visit', 'time_per_visit', 's')
                              ]}
        return stats

    def get_piwik_traffic_data(self, piwik, statistic, unit, date):
        this_week_end = date or common.end_of_current_week()
        previous_week_end = common.end_of_previous_week(this_week_end)
        method = getattr(piwik, statistic)
        current_week = method(site_id=self.site_id, date='previous1')
        previous_week = method(site_id=self.site_id, date='prior1')
        week_percent_change = common.percent_change(current_week, previous_week)
        last_four_weeks = method(site_id=self.site_id, date='previous4')
        previous_four_weeks = method(site_id=self.site_id, date='prior4')    
        month_percent_change = common.percent_change(last_four_weeks, previous_four_weeks)
        row = [{ 'current_value' : current_week,
                 'unit' : unit },  
               { 'percent_change': week_percent_change, 
                 'previous_value' : previous_week }, 
               { 'current_value' : last_four_weeks,
                 'unit' : unit },
               { 'percent_change': month_percent_change, 
                 'previous_value': previous_four_weeks } ]
        return row

    def get_traffic_data(self, stat, sources, unit, date=None):
        row = self.get_piwik_traffic_data(sources['piwik'], stat, unit, date=date)
        return row