from django.conf.urls import include, url
from django.contrib.auth import views as auth_views
from django.core.urlresolvers import reverse

from . import views

urlpatterns = [
    url(r'^tokenlogin/$', views.token_login, name='token-login'),
    url(r'^userme/$', views.UserMe_R.as_view(), name='user-me'),
    url(r'^users/$', views.UsersList.as_view(), name='users'),
    url(r'^user/(?P<email>[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+)/$', views.UserOther_R.as_view(), name='user-email'),
    url(r'^user/(?P<uid>\d+)/$', views.UserOther_R.as_view(), name='user-username'),
    url(r'^updateposition/$', views.UpdatePosition.as_view(), name='update-position'),
]
