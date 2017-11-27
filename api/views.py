# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from rest_framework import viewsets, status
from rest_framework.response import Response
from django.shortcuts import get_object_or_404

from serializers import UserSerializer, SessionSerializer
from models import SantaUser, Session
from django.contrib.auth.models import User
from django.db import transaction
import random, string


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

    def create(self, request, *args, **kwargs):
        print ('Creating session')
        data = request.data

        user = SantaUser.objects.get(pk=data['author'])

        key = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(6))
        session = Session(author=user.id, key=key)
        session.save()
        session.users.add(user)
        session.save()

        serializer = SessionSerializer(session)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def update(self, request, *args, **kwargs):
        print ('Updating session')
        data = request.data

        newUser = SantaUser.objects.get(pk=data['new_user'])
        session = Session.objects.get(pk=kwargs['pk'])

        session.users.add(newUser)
        session.save()

        serializer = SessionSerializer(session)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_200_OK, headers=headers)

