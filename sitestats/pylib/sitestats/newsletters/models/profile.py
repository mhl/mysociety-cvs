from django.db import models
from django.contrib.auth.models import User
from django.db.models import signals
from django.core.exceptions import ObjectDoesNotExist

class Profile(models.Model):
    """User profile model"""
    
    class Meta:
        app_label = 'newsletters'
        
    FORMAT_CHOICES = ((0, 'html'), 
                      (1, 'text'))
                       
    user = models.OneToOneField(User, primary_key=True)
    one_email = models.BooleanField(default=False)
    email_format = models.IntegerField(choices=FORMAT_CHOICES, default=0)

def add_user_profile(sender, **kwargs):
    """Create a user profile for any user that is saved and doesn't already have one"""
    instance = kwargs['instance']
    try:
        instance.profile
    except ObjectDoesNotExist:
        profile = Profile(user=instance)
        profile.save()

signals.post_save.connect(add_user_profile, sender=User)