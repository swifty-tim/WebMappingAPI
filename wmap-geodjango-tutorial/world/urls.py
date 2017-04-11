from django.conf.urls import include, url

from . import views

urlpatterns = [
    url(r'^countries/$', views.CountryList.as_view(), name='country_list'),
    url(r'^countries/(?P<pk>\d+)/$', views.CountryDetail.as_view(), name='country_detail'),
    url(r'^countriesmap/(?P<pk>\d+)/$', views.CountryDetailMap.as_view(), name='country_detail_map'),
    url(r'^rowcount/$', views.num_countries, name="num_countries")
]
