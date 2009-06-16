from django.db import models
from django.contrib.auth.models import User
from sitestats.newsletters.models import Newsletter

class Subscription(models.Model):
    """Subscriptions of users to newsletters"""
    class Meta:
        app_label = 'newsletters'
        
    newsletter = models.ForeignKey(Newsletter)
    user = models.ForeignKey(User)