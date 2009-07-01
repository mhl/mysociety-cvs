from sitestats.newsletters.common import *
from sitestats.newsletters.models import *
from django.template.loader import render_to_string

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
        template_params = {'traffic_table'                  : traffic_table, 
                        'piwik_previous_week_link'       : self.data['piwik_previous_week_link'],
                        'piwik_previous_four_weeks_link' : self.data['piwik_previous_four_weeks_link'],
                        'reports_in_last_month'          : self.data['reports_in_last_month']
                        }
        file_ext = format_extension(format)
        rendered = render_to_string(self.template() + '.' + file_ext, template_params)
        return rendered
     
    def generate_reports_data(self, sources, date):
        fms_api = sources['fms_api']
        month_ago = four_weeks_ago(date)
        self.data['reports_in_last_month'] = fms_api.num_reports(month_ago, date)