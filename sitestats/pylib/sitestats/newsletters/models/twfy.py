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
        self.generate_upcoming_content(sources, date)
        self.generate_referring_sites_data(sources, date)
        self.generate_search_keywords(sources, date)
        self.generate_path_data(sources, date)
        self.generate_alert_data(sources, date)
        self.generate_comment_data(sources, date)
       
    def generate_alert_data(self, sources, date):
        twfy_api = sources["twfy_api"]
        week_start = start_of_week(date)
        current_week = twfy_api.email_subscribers_count(week_start, date)
        previous_week_end = end_of_previous_week(date)
        previous_week_start = start_of_week(previous_week_end)
        previous_week = twfy_api.email_subscribers_count(previous_week_start, previous_week_end)
        week_percent_change = percent_change(current_week, previous_week)
        
        month_ago = four_weeks_ago(date)
        previous_month_end = previous_day(month_ago)
        previous_month_start = four_weeks_ago(previous_month_end)
        last_month = twfy_api.email_subscribers_count(month_ago, date)
        previous_month = twfy_api.email_subscribers_count(previous_month_start, previous_month_end)
        month_percent_change = percent_change(last_month, previous_month)
        row = ['Total number of email alert subscribers',
               { 'current_value' : current_week },  
               { 'percent_change': week_percent_change, 
                 'previous_value' : previous_week }, 
               { 'current_value' : last_month },
               { 'percent_change': month_percent_change, 
                 'previous_value': previous_month } ]
        self.data['traffic_rows'].insert(-1, row)
        alerts = twfy_api.top_email_subscriptions(week_start, date, limit=5)
        alerts = [self.get_speakers(alert, sources) for alert in alerts]
        self.data['alerts'] = alerts
    
    def generate_comment_data(self, sources, date):
        twfy_api = sources["twfy_api"]
        week_start = start_of_week(date)
        comment_pages = twfy_api.top_comment_pages(week_start, date, limit=5)
        formatted_comment_pages = []
        for comment_page in comment_pages:
             formatted_comment_pages.append({'current_value' : comment_page, 
                                             'link': "%s/%s" % (self.base_url, comment_page)})
        self.data['comment_pages'] = formatted_comment_pages
        
    def render_data(self, format):
     traffic_table = self.render_traffic_data(format)
     referring_sites_table = render_table(format, self.data['referring_sites_headers'], self.data['referring_sites_rows'])
     upcoming_tables = []
     for upcoming_data in self.data['upcoming_data']:
         upcoming_tables.append(render_table(format, upcoming_data['headers'], upcoming_data['rows']))
     internal_search_keywords = [format_value(format, params) for params in self.data['internal_search_keywords']]     
     comment_pages = [format_value(format, params) for params in self.data['comment_pages']] 
     path_table = render_table(format, self.data['path_headers'], self.data['path_rows'])
     template_params = {'traffic_table'                  : traffic_table, 
                        'piwik_previous_week_link'       : self.data['piwik_previous_week_link'],
                        'piwik_previous_four_weeks_link' : self.data['piwik_previous_four_weeks_link'],
                        'referring_sites_table'          : referring_sites_table, 
                        'search_keywords'                : self.data['search_keywords'], 
                        'internal_search_keywords'       : internal_search_keywords,  
                        'upcoming_tables'                : upcoming_tables, 
                        'path_table'                     : path_table, 
                        'alerts'                         : self.data['alerts'], 
                        'comment_pages'                  : comment_pages}
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
        self.data['internal_search_keywords'] = self.format_internal_search_keywords(internal_search_keywords, sources)
        
    def format_internal_search_keywords(self, keywords, sources):
        formatted_keywords = []
        for keyword in keywords:
            formatting_params = {'link' : "%s/search%s" % (self.base_url, keyword)}
            keyword = keyword.split('&')[0]
            keyword = re.sub('/\?s=', '', keyword)
            keyword = unquote_plus(keyword)
            keyword = self.get_speakers(keyword, sources)
            formatting_params['current_value'] = keyword
            formatted_keywords.append(formatting_params)
        return formatted_keywords
        
    def get_speakers(self, text, sources):
        twfy_api = sources['twfy_api']
        matches = re.finditer('speaker:(\d+)', text)
        if matches:
            for match in matches:
                person_id =  match.group(1)
                person_name = twfy_api.person_name(person_id)
                text = re.sub('speaker:\d+', 'speaker:' + person_name, text)
        return text
        
    def generate_path_data(self, sources, date):
        piwik = sources['piwik']
        path_roots = piwik.top_roots_and_percent_visits(site_id=self.site_id, date="previous1", limit=10)
        headers = ['area of the site', '% visits that included this feature']
        rows = []
        for path, percent_of_visits in path_roots:
            row = [path, {'current_value' : percent_of_visits, 'unit' : '%'}]
            rows.append(row)
        self.data['path_headers'] = headers
        self.data['path_rows'] = rows
            
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