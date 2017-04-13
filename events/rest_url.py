from django.conf.urls import include, url
from django.contrib.auth import views as auth_views
from django.core.urlresolvers import reverse

from . import views, rest_views

urlpatterns = [
    url(r'activity/', rest_views.EventRetrieveAPI.as_view(), name="activity"),
    url(r'^token-auth/$', rest_views.obtain_auth_token, name='obtain-token-auth'),
    url(r'^register', rest_views.register, name="register"),
]