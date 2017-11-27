# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from rest_framework import viewsets
from serializers import UserSerializer, SessionSerializer
from models import SantaUser, Session


class UsersList(viewsets.ModelViewSet):
    queryset = SantaUser.objects.all()
    serializer_class = UserSerializer


class SessionsList(viewsets.ModelViewSet):
    queryset = Session.objects.all()
    serializer_class = SessionSerializer
