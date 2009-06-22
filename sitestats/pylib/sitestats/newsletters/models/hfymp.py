from sitestats.newsletters.models import *

class HFYMPNewsletter(Newsletter):
    
    class Meta:
        app_label = 'newsletters'
        
    site_name = 'HearFromYourMP'  
    site_id = None
    data = {}
    formats = {}
    sites = {}
    
    def template(self):
        return 'hfymp'
    