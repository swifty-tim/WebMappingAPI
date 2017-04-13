# -*- coding: utf-8 -*-
from rest_framework import permissions, generics, authentication, status
from django.contrib.auth import authenticate, login, logout, get_user_model
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from .models import Event, Attendees
from .serializers import EventSerializer, AttendeesSerializer

from django.shortcuts import render


class EventRetrieveAPI(generics.ListAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = EventSerializer

    def get_queryset(self):
        return Event.objects.filter(owner=1)


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