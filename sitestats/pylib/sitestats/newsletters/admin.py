from sitestats.newsletters.models import Subscription, CommonBaseMeasuresNewsletter, Profile
from django.contrib import admin
from django.contrib.auth.models import User, Group
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import ugettext, ugettext_lazy as _

class ProfileInline(admin.StackedInline):
    model = Profile
    fk_name = 'user'
    max_num = 1
    can_delete = False

class SubscriptionInline(admin.StackedInline):
    model = Subscription
    fk_name = 'user'
    
class CustomUserAdmin(UserAdmin):
    inlines = [ProfileInline, SubscriptionInline,]
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        (_('Personal info'), {'fields': ('first_name', 'last_name', 'email')}),
    )

admin.site.unregister(Group)    
admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)

