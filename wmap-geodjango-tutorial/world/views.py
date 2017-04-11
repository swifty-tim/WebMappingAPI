from django.shortcuts import render
from django.views import generic
from django.views.decorators.http import require_safe
from . import models
from . import forms

from django.http import HttpResponse

from djgeojson.views import GeoJSONLayerView

class CountryList(generic.ListView):
    template_name = "world/country_list.html"
    # queryset = models.WorldBorder.objects.all().order_by('name')

    def get_queryset(self):
        return models.WorldBorder.objects.all().order_by('name')


class CountryDetail(generic.DetailView):
    # queryset = models.WorldBorder.objects.all().order_by('name')
    model = models.WorldBorder
    template_name = "world/country_detail.html"
    form_class = forms.MyGeoForm


    # @require_safe
    # def dispatch(self, *args, **kwargs):
    #     return super(CountryDetail, self).dispatch(*args, **kwargs)


class CountryDetailMap(generic.DetailView):
    model = models.WorldBorder
    template_name = "world/base.html"


def num_countries(request):

    count = models.WorldBorder.objects.count()

    return_string = "There are {} countries in our World".format(count)
    return HttpResponse(return_string)



