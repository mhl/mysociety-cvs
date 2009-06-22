from sitestats.newsletters.models import *

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

        
