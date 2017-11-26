# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from rest_framework import viewsets
from serializers import UserSerializer
from models import SantaUser


class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = SantaUser.objects.all()
    serializer_class = UserSerializer
