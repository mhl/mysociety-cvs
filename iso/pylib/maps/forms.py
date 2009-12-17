from django import forms

from django.contrib.localflavor.uk.forms import UKPostcodeField

class PostcodeForm(forms.Form):
    # This postcode field will uppercase the postcode and add a
    # space in the appropriate place.
    postcode = UKPostcodeField()
    
