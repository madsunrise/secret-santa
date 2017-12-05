# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.contrib.auth.models import User
from django.db import models
import datetime


# Create your models here.

class SantaUser(models.Model):
    user = models.OneToOneField(User)
    wish = models.TextField()


class Session(models.Model):
    author = models.IntegerField()  # author id
    users = models.ManyToManyField(SantaUser)
    date = models.DateTimeField(default=datetime.datetime.now)
    key = models.CharField(max_length=6)
    alreadyPlayed = models.IntegerField(default=0)
