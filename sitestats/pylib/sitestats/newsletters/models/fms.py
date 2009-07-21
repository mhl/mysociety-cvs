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
        Newsletter.generate_data(self,sources, date)    
        self.generate_reports_data(sources, date) 

    def template_params(self, format):
        template_params = Newsletter.template_params(self, format)
        reports_table = render_table(format, self.data['reports_headers'], self.data['reports_rows'])
        template_params.update({'reports_table'            : reports_table, 
                                'service_counts'           : self.data['service_counts'],
                                'top_categories_this_week' : self.data['top_categories_this_week'],
                                'top_councils_this_week'   : self.data['top_councils_this_week']})
        return template_params
        
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
            row = self.generate_stats_row(method, date, header, unit)
            rows.append(row)
        self.data['reports_headers'] = headers
        self.data['reports_rows'] = rows
        self.data['service_counts'] = fms_api.service_counts(week_start, date)
        self.data['top_categories_this_week'] = fms_api.top_categories(week_start, date, limit=5)
        self.data['top_councils_this_week'] = fms_api.top_councils(week_start, date, limit=5)