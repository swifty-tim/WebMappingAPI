from django.contrib.gis import forms
from . import models

class MyGeoForm(forms.Form):
    class Meta:
        model = models.WorldBorder

    mpoly = forms.MultiPolygonField(widget=
        forms.OSMWidget(attrs={'map_width': 800, 'map_height': 500}))