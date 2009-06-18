from django.db import models
from sitestats.newsletters import common

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

    def __unicode__(self):
        return self.name
    
    def render(self, format, sources, date=None):
        return "Abstract"

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
            row += self.get_traffic_data(stat, sources, date)
            rows.append(row)

        self.data['headers'] = headers
        self.data['rows'] = rows

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

    def get_piwik_traffic_data(self, piwik, statistic, date):
        this_week_end = date or common.end_of_current_week()
        previous_week_end = common.end_of_previous_week(this_week_end)
        method = getattr(piwik, statistic)
        current_week = method(site_id=self.site_id, date='previous1')
        previous_week = method(site_id=self.site_id, date='prior1')
        week_percent_change = common.percent_change(current_week, previous_week)
        last_four_weeks = method(site_id=self.site_id, date='previous4')
        previous_four_weeks = method(site_id=self.site_id, date='prior4')    
        month_percent_change = common.percent_change(last_four_weeks, previous_four_weeks)
        row = [current_week, 
               { 'percent_change': week_percent_change, 
                 'previous_value' : previous_week }, 
               last_four_weeks, 
               { 'percent_change': month_percent_change, 
                 'previous_value': previous_four_weeks } ]
        return row

    def get_traffic_data(self, stat, sources, date=None):
        row = self.get_piwik_traffic_data(sources['piwik'], stat, date=date)
        return row