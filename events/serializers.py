from . import models
from EventAPI import settings
from rest_framework import serializers
from rest_framework_gis import serializers as geo_serializers
from rest_framework.reverse import reverse
from django.contrib.auth import get_user_model
from django.contrib.gis.geos import GEOSGeometry, LineString, Point, Polygon


class EventSerializer(geo_serializers.GeoFeatureModelSerializer):

    url = serializers.SerializerMethodField()

    class Meta:
        model = get_user_model()
        geo_field = "location"
        fields = ('name', 'time', 'description', 'location', 'owner')

    def get_url(self, obj):
        return self.context["request"].build_absolute_uri(reverse("rest:user-username", kwargs={"uid": obj.pk}))


class AttendeesSerializer(geo_serializers.GeoFeatureModelSerializer):

    url = serializers.SerializerMethodField()

    class Meta:
        model = get_user_model()
        geo_field = "location"
        fields = ('attendee', 'event')

    def get_url(self, obj):
        return self.context["request"].build_absolute_uri(reverse("rest:user-username", kwargs={"uid": obj.pk}))
