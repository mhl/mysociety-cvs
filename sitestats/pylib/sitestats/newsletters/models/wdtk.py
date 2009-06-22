from sitestats.newsletters.models import *

class WDTKNewsletter(Newsletter):
    
    class Meta:
        app_label = 'newsletters'
    
    site_name = 'WhatDoTheyKnow'  
    site_id = None
    data = {}
    formats = {}
    sites = {}

    def template(self):
        return 'wdtk'