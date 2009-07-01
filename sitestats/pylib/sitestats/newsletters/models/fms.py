from sitestats.newsletters.common import *
from sitestats.newsletters.models import *
from django.template.loader import render_to_string
from sitestats.newsletters.formatting import render_table, format_value

class FMSNewsletter(Newsletter):
    
    class Meta:
        app_label = 'newsletters'
        
    site_name = 'FixMyStreet'  
    site_id = None
    data = {}
    formats = {}
    sites = {}
    
    def template(self):
        return 'fms'

    def generate_data(self, sources, date):
        self.generate_traffic_data(sources, date)       
        self.generate_reports_data(sources, date) 

    def render_data(self, format):
        '''Default content for a newsletter - a table of site traffic stats'''
        traffic_table = self.render_traffic_data(format)
        reports_table = render_table(format, self.data['reports_headers'], self.data['reports_rows'])
        
        template_params = {'traffic_table'                   : traffic_table, 
                            'piwik_previous_week_link'       : self.data['piwik_previous_week_link'],
                            'piwik_previous_four_weeks_link' : self.data['piwik_previous_four_weeks_link'],
                            'reports_table'                  : reports_table, 
                            'service_counts'                 : self.data['service_counts'],
                            'top_categories_this_week'       : self.data['top_categories_this_week']
                        }
        file_ext = format_extension(format)
        rendered = render_to_string(self.template() + '.' + file_ext, template_params)
        return rendered
        
    def generate_reports_data(self, sources, date):
        fms_api = sources['fms_api']
        week_start = start_of_week(date)
        month_ago = four_weeks_ago(date)
        rows = []
        stats = [('Problems reported', 'num_reports', ''),
                 ('Problems fixed',    'num_fixes',   '')]
        headers = ['', 'This week', '% change on last week', 'last 4 weeks', '% change on last 4 weeks']
        
        for (header, stat, unit) in stats: 
            method = getattr(fms_api, stat)
            row = self.generate_stats_row(method, date, header)
            rows.append(row)
        self.data['reports_headers'] = headers
        self.data['reports_rows'] = rows
        self.data['service_counts'] = fms_api.service_counts(week_start, date)
        self.data['top_categories_this_week'] = fms_api.top_categories(week_start, date, limit=5)