from sitestats.newsletters.models import *

class PBNewsletter(Newsletter):
    
    class Meta:
        app_label = 'newsletters'
    
    site_name = 'PledgeBank'  
    site_id = None
    data = {}
    formats = {}
    sites = {}
    
    def template(self):
        return 'pb'