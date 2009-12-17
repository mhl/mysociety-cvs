from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect

import simpledb

import mysociety.mapit

import forms
import models
import storage

def enter_postcode(request, form_class=forms.PostcodeForm):
    if request.method == 'POST':
        form = form_class(request.POST)
        if form.is_valid():
            postcode = form.cleaned_data['postcode']

            # FIXME - check that we have a location for the postcode and
            # that it isn't in Northern Ireland
            return HttpResponseRedirect('/postcode/%s' %postcode)
    else:
        form = form_class()

    return render_to_response('index.html', {
        'form': form,
    })

def map_postcode(request, target_postcode):
    # Check that the postcode is OK, by using
    # the regex from UKPostcodeField
    # FIXME - probably don't need the whole form here, 
    # could just use the field.
    
    form = forms.PostcodeForm(dict(postcode=target_postcode))
    if not form.is_valid():
        # Redirect to the front page.
        # FIXME - it would be better to have a nice error message here.
        return HttpResponseRedirect('/')

    target_postcode = form.cleaned_data['postcode']

    location = mysociety.mapit.get_location(target_postcode)

    map_obj= models.MapObject(
        target_e = int(location['easting']),
        target_n = int(location['northing']),
        arrive_by = True, # FIXME - hardcoded
        target_time = 9*60,#FIXME - hardcoded. request.REQUEST['target_time'],
        target_limit_time = 5*60,# FIXME - hardcoded. request.REQUEST['target_limit_time'],
        postcode = target_postcode,
        )

    return map_from_object(request, map_obj)

def map_from_object(request, map_object):
    
    try:
        this_map = models.MapObject.objects.get(map_object.get_identifier())
    except simpledb.ItemDoesNotExist:
        # Map is not yet in simpledb - we need to queue it.
        queue = storage.get_map_creation_queue()
        queue.queue_map(map_object)
        this_map = map_object

        return render_to_response('map-pleasewait.html', {})

    if this_map.working_finished:
        iso_file = this_map.get_iso_file()

        import pdb;pdb.set_trace()
        
    else:
        return render_to_response('map-pleasewait.html', {})



# From index.cgi
def map_complete(map_object, invite):
    # Check there is a route file
    filename = os.path.join(tmpwork, '%s.iso' % str(map_object.id))
    if not os.path.exists(filename):
        return page.render_to_response('map-noiso.html', { 'map_id' : map_object.id })
    # Let's show the map
    if map_object.target_direction == 'arrive_by':
        initial_minutes = abs(map_object.target_time - map_object.target_limit_time) - 60
    else:
        initial_minutes = 60
    return page.render_to_response('map.html', {
        'map': map_object,
        'tile_web_host' : mysociety.config.get('TILE_WEB_HOST'),
        'show_max_minutes': abs(map_object.target_time - map_object.target_limit_time),
        'initial_minutes': initial_minutes,
        'invite': invite,
        'show_dropdown': len(invite.postcodes) > 3,
    })
