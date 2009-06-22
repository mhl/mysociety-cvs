from sitestats.newsletters.models import *

class WTTNewsletter(Newsletter):
    
    class Meta:
        app_label = 'newsletters'
    
    site_name = 'WriteToThem'  
    site_id = None
    data = {}
    formats = {}
    sites = {}
    
    def template(self):
        return 'wtt'