from django.db import models

class Newsletter(models.Model):
    
    class Meta:
        app_label = 'newsletters'
        
    name = models.CharField(max_length=255)

    def __unicode__(self):
        return self.name
    
    def render(self, format, sources, date=None):
        return "Abstract"
