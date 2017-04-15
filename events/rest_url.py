from django.conf.urls import include, url
from django.contrib.auth import views as auth_views
from django.core.urlresolvers import reverse
from rest_framework.urlpatterns import format_suffix_patterns
from . import rest_views

urlpatterns = [
    url(r'events/$', rest_views.EventList.as_view(), name="events"),
    url(r'events/(?P<pk>[0-9]+)/$', rest_views.EventDetail.as_view(), name="events1"),
    url(r'attendee/$', rest_views.AttendeeList.as_view(), name="attendee"),
    url(r'attendeesEvent/(?P<pk>[0-9]+)/$', rest_views.AttendeesEvents.as_view(), name="attendeeEvents"),
    url(r'attendee/(?P<id>[0-9]+)/$', rest_views.AttendeeDetail.as_view(), name="attendee1"),
    url(r'^token-auth/$', rest_views.obtain_auth_token, name='obtain-token-auth'),
    url(r'^register', rest_views.register, name="register"),
]

urlpatterns = format_suffix_patterns(urlpatterns)