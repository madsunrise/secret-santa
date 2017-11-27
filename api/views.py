# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from rest_framework import viewsets, status
from rest_framework.response import Response
from django.shortcuts import get_object_or_404

from serializers import UserSerializer, SessionSerializer
from models import SantaUser, Session
from django.contrib.auth.models import User
from django.db import transaction


class UserViewSet(viewsets.ModelViewSet):
    queryset = SantaUser.objects.all()
    serializer_class = UserSerializer

    def create(self, request, *args, **kwargs):
        data = request.data

        with transaction.atomic():
            user = User(
                username=data['username'],
                email=data['email'],
                password=data['password']
            )
            user.clean()
            user.save()

            santaUser = SantaUser.objects.create(
                user=user,
                wish=data['wish']
            )

        serializer = UserSerializer(santaUser)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def retrieve(self, request, *args, **kwargs):
        queryset = SantaUser.objects.all()
        user = get_object_or_404(queryset, pk=kwargs['pk'])
        serializer = UserSerializer(user)
        return Response(serializer.data)


class SessionViewSet(viewsets.ModelViewSet):
    queryset = Session.objects.all()
    serializer_class = SessionSerializer
