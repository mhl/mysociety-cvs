from sitestats.newsletters.common import *
from sitestats.newsletters.models import *
from sitestats.newsletters.formatting import render_table
from django.template.loader import render_to_string

class FMSNewsletter(Newsletter):
    
    class Meta:
        app_label = 'newsletters'
        
    data = {}
    formats = {}
    sites = {}
    site_id = None
    site_name = 'FixMyStreet'  
    
    def render(self, format, sources, date=None):
        """Returns the text for a FixMyStreet email in text/html"""
        self.set_site_id(sources)
        if not self.formats.get(format):
            if not self.data:
                self.generate_traffic_data(sources, date)
            traffic_table = render_table(format, self.data['headers'], self.data['rows'])            
            template_params = {'traffic_table' : traffic_table}
            file_ext = format_extension(format)
            rendered = render_to_string('twfy.' + file_ext, template_params)
            self.formats[format] = rendered
        return self.formats[format]
        
