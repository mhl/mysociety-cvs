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
     
    def template(self):
        return 'twfy'
           
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
        self.generate_referring_sites_data(sources, date)
        self.generate_search_keywords(sources, date)
       
    def render_data(self, format):
     traffic_table = render_table(format, self.data['traffic_headers'], self.data['traffic_rows'])  
     referring_sites_table = render_table(format, self.data['referring_sites_headers'], self.data['referring_sites_rows'])
     template_params = {'traffic_table'         : traffic_table, 
                        'referring_sites_table' : referring_sites_table, 
                        'search_keywords'       : self.data['search_keywords']}
     file_ext = format_extension(format)
     rendered = render_to_string(self.template() + '.' + file_ext, template_params)
     return rendered
     
    def generate_search_keywords(self, sources, date):
        piwik = sources['piwik']
        search_keywords = piwik.top_search_keywords(site_id=self.site_id, date=date, limit=20)
        self.data['search_keywords'] = search_keywords
        
    def generate_referring_sites_data(self, sources, date):
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
        self.data['referring_sites_headers'] = headers
        self.data['referring_sites_rows'] = rows