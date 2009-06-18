from sitestats.newsletters.common import *
from sitestats.newsletters.models import *
from sitestats.newsletters.formatting import render_table
from django.template.loader import render_to_string

class TWFYNewsletter(Newsletter):
    
    class Meta:
        app_label = 'newsletters'
    
    site_name = 'TheyWorkForYou'
    site_id = None
    data = {}
    formats = {}
    sites = {}
        
    def render(self, format, sources, date=None):
        """Returns the text for a TWFY email in text/html"""
        self.set_site_id(sources)
        if not self.formats.get(format):
            if not self.data:
                self.generate_traffic_data(sources, date)
            traffic_table = render_table(format, self.data['headers'], self.data['rows'])            
            template_params = {'traffic_table'         : traffic_table, 
                               'referring_sites_table' : self.referring_sites_table(format, sources, date) }
            file_ext = format_extension(format)
            rendered = render_to_string('twfy.' + file_ext, template_params)
            self.formats[format] = rendered
        return self.formats[format]

    def referring_sites_table(self, format, sources, date):
        piwik = sources['piwik']
        top_referrers = piwik.top_referrers(site_id=self.site_id, date=date, limit=10)
        headers = ['Referring website', 
                   '% of visits this week', 
                   '% change on last week', 
                   'last 4 weeks', 
                   '% change on last 4 weeks']
        rows = []
        for referrer in top_referrers: 
            current_week = piwik.percent_visits_from_referrer(site_id=self.site_id, referrer=referrer, date='previous1')
            previous_week = piwik.percent_visits_from_referrer(site_id=self.site_id, referrer=referrer, date='prior1')
            week_percent_change = percent_change(current_week, previous_week)
            last_four_weeks = piwik.percent_visits_from_referrer(site_id=self.site_id, referrer=referrer, date='previous4')
            previous_four_weeks = piwik.percent_visits_from_referrer(site_id=self.site_id, referrer=referrer, date='prior4')    
            month_percent_change = percent_change(last_four_weeks, previous_four_weeks)
            row = [referrer, 
                   {'current_value' : current_week, 
                    'unit' : '%'}, 
                   { 'percent_change': week_percent_change, 
                     'previous_value' : previous_week, 
                     'unit' : '%'},
                   {'current_value' : last_four_weeks, 
                    'unit' : '%'},
                   { 'percent_change': month_percent_change, 
                     'previous_value': previous_four_weeks, 
                     'unit' : '%' }]
            rows.append(row)
        table = render_table(format, headers, rows)
        return table