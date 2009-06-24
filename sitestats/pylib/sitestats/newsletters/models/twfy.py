from sitestats.newsletters.common import *
from sitestats.newsletters.models import *
from sitestats.newsletters.formatting import render_table, format_value
from django.template.loader import render_to_string
from urllib import unquote_plus
import re

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
        self.generate_upcoming_content(sources, date)
       
    def render_data(self, format):
     traffic_table = self.render_traffic_data(format)
     referring_sites_table = render_table(format, self.data['referring_sites_headers'], self.data['referring_sites_rows'])
     upcoming_tables = []
     for upcoming_data in self.data['upcoming_data']:
         upcoming_tables.append(render_table(format, upcoming_data['headers'], upcoming_data['rows']))
     internal_search_keywords = [format_value(format, params) for params in self.data['internal_search_keywords']]     
     template_params = {'traffic_table'                  : traffic_table, 
                        'piwik_previous_week_link'       : self.data['piwik_previous_week_link'],
                        'piwik_previous_four_weeks_link' : self.data['piwik_previous_four_weeks_link'],
                        'referring_sites_table'          : referring_sites_table, 
                        'search_keywords'                : self.data['search_keywords'], 
                        'internal_search_keywords'       : internal_search_keywords,  
                        'upcoming_tables'                : upcoming_tables}
     file_ext = format_extension(format)
     rendered = render_to_string(self.template() + '.' + file_ext, template_params)
     return rendered
     
    def generate_upcoming_content(self, sources, date):
        piwik = sources['piwik']
        stats = [('MP pages',        'mp',      ['/index', -1], []), 
                 ('debate pages',    'debates', [], ['\?id=']), 
                 ('Written Answers', 'wrans',   [], ['\?id=.*\.h'])]
        for heading, path, exclude, include in stats:         
            top_values = piwik.top_children(self.site_id, path, date="previous1", limit=5, exclude=exclude, include=include)
            upcoming_values = piwik.upcoming_children(self.site_id, path, limit=5, exclude=exclude, include=include)
            headers = ['Top %s' % (heading), 'Upcoming %s' % (heading)]
            rows = []
            base_url = self.base_url
            for top, upcoming in  zip(top_values, upcoming_values):
                top = re.sub('^/', '', top)
                upcoming = re.sub('^/', '', upcoming)
                rows.append([{'current_value' : top, 
                              'link': "%s/%s/%s" % (base_url, path, top)},
                             {'current_value' : upcoming, 
                              'link': "%s/%s/%s" % (base_url, path, upcoming)} ])
            self.data.setdefault('upcoming_data', []).append({'headers' : headers, 'rows' : rows})
            
    def generate_search_keywords(self, sources, date):
        piwik = sources['piwik']
        search_keywords = piwik.upcoming_search_keywords(site_id=self.site_id, limit=20)
        internal_search_keywords = piwik.upcoming_children(site_id=self.site_id, 
                                                           root='search',  
                                                           limit=20, 
                                                           exclude=[], 
                                                           include=['/\?s=.'])
        self.data['search_keywords'] = search_keywords
        self.data['internal_search_keywords'] = self.format_internal_search_keywords(internal_search_keywords)
        
    def format_internal_search_keywords(self, keywords):
        formatted_keywords = []
        for keyword in keywords:
            formatting_params = {'link' : "%s/search%s" % (self.base_url, keyword)}
            keyword = keyword.split('&')[0]
            keyword = re.sub('/\?s=', '', keyword)
            formatting_params['current_value'] = unquote_plus(keyword)
            formatted_keywords.append(formatting_params)
            
        return formatted_keywords
        
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