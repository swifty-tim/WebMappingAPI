# -*- coding: utf-8 -*-
from . import models
from . import serializers
from rest_framework import permissions
from EventAPI import settings

from django.contrib.auth import authenticate, login, logout, get_user_model
from rest_framework import permissions, authentication, status, generics
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework import exceptions
from django.contrib.auth import get_user_model
from django.contrib.gis.geos import GEOSGeometry, LineString, Point, Polygon
from rest_framework.authtoken.models import Token

from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
# from rest_framework.decorators import api_view, permission_classes
from django.views.decorators.csrf import csrf_exempt, ensure_csrf_cookie
from django.utils.decorators import method_decorator


class EventList(APIView):
    """
    List all snippets, or create a new event.
    """
    def get(self, request, format=None):
        snippets = models.Event.objects.all()
        serializer = serializers.EventSerializer(snippets, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = serializers.EventSerializer(data=request.data)
        if serializer.is_valid():
            try:
                lat1 = float(self.request.data.get("lat", False))
                lon1 = float(self.request.data.get("lon", False))
                # lat2 = float(self.request.query_params.get("lat", False))
                # lon2 = float(self.request.query_params.get("lon", False))
                if lat1 and lon1:
                    point = Point(lon1, lat1)
                # elif lat2 and lon2:
                #     point = Point(lon2, lat2)
                else:
                    point = None

                if point:
                    # serializer.instance.location = point
                    serializer.save(location=point)
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            except:
                pass
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class EventDetail(APIView):
    """
    Retrieve, update or delete a snippet event.
    """

    def get_object(self, pk):
        try:
            return models.Event.objects.get(pk=pk)
        except models.Event.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        event = self.get_object(pk)
        serializer = serializers.EventSerializer(event)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        event = self.get_object(pk)
        serializer = serializers.EventSerializer(event, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        snippet = self.get_object(pk)
        snippet.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)




class AttendeeList(APIView):
    """
    List all snippets, or create a new attendee.
    """
    def get(self, request, format=None):
        attendees = models.Attendees.objects.all()
        serializer = serializers.AttendeesSerializer(attendees, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = serializers.AttendeesSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AttendeeDetail(APIView):
    """
    Retrieve, update or delete a attendee instance.
    """

    def get_object(self, pk):
        try:
            return models.Attendees.objects.get(event=pk)
        except models.Attendees.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        attendee = self.get_object(pk)
        serializer = serializers.AttendeesSerializer(attendee)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        attendee = self.get_object(pk)
        serializer = serializers.AttendeesSerializer(attendee, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        attendee = self.get_object(pk)
        attendee.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class AttendeesEvents(APIView):
    """
    Retrieve  AttendeeEvents instance.
    """

    def get_object(self, pk):
        try:
            return models.Attendees.filter(event=pk)
        except models.Attendees.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        attendees = self.get_object(pk)
        serializer = serializers.AttendeesSerializer(attendees, many=True)
        return Response(serializer.data)


@api_view(["GET", ])
@permission_classes((permissions.AllowAny,))
def obtain_auth_token(request):
    if (not request.GET["username"]) or (not request.GET["password"]):
        return Response({"message": "Please provide username and password"}, status=status.HTTP_400_BAD_REQUEST)

    user = authenticate(username=request.GET["username"], password=request.GET["password"])

    if user:
        if user.is_active:
            try:
                token = Token.objects.get_or_create(user=user)
                return Response({"token": "{}".format(token[0])}, status=status.HTTP_200_OK)
            except Exception as e:
                return Response({"message": "Could not generate token"})
        else:
            return Response({"message": "This account is not active."}, status=status.HTTP_400_BAD_REQUEST)
    else:
        return Response({"message": "Incorrect username or password"}, status=status.HTTP_400_BAD_REQUEST)


# Create your views here.
@api_view(['POST', ])
@permission_classes((permissions.AllowAny,))
def register(request):
    try:
        username = request.data['username']
        email = request.data['email']
        first_name = request.data['first_name']
        last_name = request.data['last_name']
        password = request.data['password']

    except KeyError:  # i.e incorrect details were sent
        return Response({"message": "Please send the correct details"}, status=status.HTTP_400_BAD_REQUEST)

    try:
        user = get_user_model().objects.get(username=username)
        if user:
            return Response({"message": "User already exists"}, status=status.HTTP_400_BAD_REQUEST)
    except get_user_model().DoesNotExist:
        user = get_user_model().objects.create_user(username=username)
        user.set_password(password)
        user.email = email
        user.first_name = first_name
        user.last_name = last_name
        user.save()
        return Response({"message": "User successfully added"})