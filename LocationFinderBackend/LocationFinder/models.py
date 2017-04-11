from __future__ import unicode_literals
from django.utils import timezone
from django.contrib.gis.geos import Point

from django.contrib.gis.db import models
from django.contrib.gis import geos
from django.contrib.auth.models import AbstractUser

from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token


class User(AbstractUser):
    created = models.DateTimeField(
        auto_now_add=True
    )
    modified = models.DateTimeField(
        auto_now=True
    )

    def __str__(self):
        return "{}, ({}), last seen at {}, mod={}" \
            .format(self.username, self.get_full_name(), self.created, self.modified)


class Event(models.Model):
    name = models.CharField(
        max_length=100,
        blank=True,
        verbose_name="name"
    )
    time = models.DateTimeField(
        auto_now_add=True
    )
    description = models.CharField(
        max_length=255,
        blank=True,
        verbose_name="description"
    )
    location = models.PointField(
        verbose_name="event location",
        blank=True,
        null=True
    )
    owner = models.ForeignKey(
        User,
        related_name="list_owner",
        verbose_name="owner",
        on_delete=models.CASCADE
    )
    created = models.DateTimeField(
        auto_now_add=True
    )
    modified = models.DateTimeField(
        auto_now=True
    )


class Attendees(models.Model):
    attendee = models.ForeignKey(
        User,
        related_name="attendee_name",
        verbose_name="attendee",
        on_delete=models.CASCADE
    )
    event = models.ForeignKey(
        Event,
        related_name="event_name",
        verbose_name="event",
        on_delete=models.CASCADE
    )
    created = models.DateTimeField(
        auto_now_add=True
    )
    modified = models.DateTimeField(
        auto_now=True
    )

    def __str__(self):
        return "{} owned by {}".format(self.attendee.first_name, self.event.name)


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)
