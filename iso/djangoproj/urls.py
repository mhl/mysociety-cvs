from django.conf.urls.defaults import *

import maps.views

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    (r'^$', maps.views.enter_postcode),
#    (r'^/station/([A-Z0-9]+)$',   /index.cgi?station_id=$1 [QSA]
#    (r'^/grid/([0-9]+)/([0-9]+)$',   /index.cgi?target_e=$1&target_n=$2 [QSA]
    (r'^postcode/(?P<target_postcode>[0-9A-Z ]+)$', maps.views.map_postcode),
#    (r'^/stats$',   /index.cgi?stats=1 [QSA]
#    (r'^/help$',      /static.cgi?page=faq [QSA]
#    (r'^/contact$',   /contact.cgi [QSA]
    
    # Invites
#    (r'^/[Tt]/([0-9A-Za-z]{16,18}).*$', /invite.cgi?token=$1
#    (r'^/signup$',    /invite.cgi?signup=1 [QSA]
#    (r'^/invite$',    /invite.cgi [QSA]
    
#    (r'^/cloudmade-tiles/([^/]*)/([^/]*)/([^/]*)\.png$',   /proxy.cgi?z=$1&x=$2&y=$3
    


    # Example:
    # (r'^mapumental/', include('mapumental.foo.urls')),

    # Uncomment the admin/doc line below and add 'django.contrib.admindocs' 
    # to INSTALLED_APPS to enable admin documentation:
    # (r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # (r'^admin/(.*)', admin.site.root),
)
