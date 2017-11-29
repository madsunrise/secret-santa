# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from rest_framework import viewsets, status
from rest_framework.response import Response
from django.core.mail import send_mail

from serializers import UserSerializer, SessionSerializer
from models import SantaUser, Session
from django.contrib.auth.models import User
from django.db import transaction
import random, string


class UserViewSet(viewsets.ModelViewSet):
    queryset = SantaUser.objects.none()
    serializer_class = UserSerializer

    def create(self, request, *args, **kwargs):
        data = request.data

        with transaction.atomic():
            user = User(
                username=randomString(6),
                first_name=data['name'],
                email=data['email'],
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
        # queryset = SantaUser.objects.all()
        # user = get_object_or_404(queryset, pk=kwargs['pk'])
        # serializer = UserSerializer(user)
        # return Response(serializer.data)
        return Response(status=status.HTTP_403_FORBIDDEN)


class SessionViewSet(viewsets.ModelViewSet):
    queryset = Session.objects.none()
    serializer_class = SessionSerializer

    def retrieve(self, request, *args, **kwargs):
        return Response(status=status.HTTP_403_FORBIDDEN)

    def create(self, request, *args, **kwargs):
        print ('Creating session')
        data = request.data

        user = SantaUser.objects.get(pk=data['author'])

        key = randomId(4)
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
        sendConfirmationEmail(newUser.user.email)
        return Response(serializer.data, status=status.HTTP_200_OK, headers=headers)


def randomString(length):
    return ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(length))


def randomId(length):
    return ''.join(random.choice(string.digits) for _ in range(length))


def sendConfirmationEmail(email):
    send_mail(
        'Тайный Санта',
        'Ура! Ты был зарегистрирован в Тайном Санте 2018! Держи случайный анекдот: \n' + randomJoke() + '\n\nС уважением, ваш Санта',
        '2017.secret.santa.2018@gmail.com',
        [email],
        fail_silently=False,
    )


def randomJoke():
    jokes = [
        '''Разговор двух блондинок.
— Представляешь! Говорят, что этот Новый год выпадет на пятницу!
— Да-а! Только бы не на тринадцатое!''',
        '''Приходит Дед Мороз к психиатру и говорит "Помогите доктор, я в себя не верю"!''',
        '''В этом году письмо буду писать Снегурочке... )))) Она как женщина должна меня понять...!''',
        '''Три возраста мужчины:
- Он надеется, что его желания исполнит Дед Мороз.
- Он надеется, что его желания исполнит Снегурочка.
- Он надеется, что его желания исполнит Дед Мороз, если придет Снегурочка.''',
        '''- Мама, мама! Ёлка горит!
- Сынок, не горит, а сияет.
- Мама, мама! Шторы сияют!''',
        '''Дорогой Дедушка Мороз...
         Я была хорошей девочкой весь год... Хм.. . Ну почти весь год... Хм.. . Ну иногда...
          Хм.. . Ну пару раз то точно была... ОЙ ДА ЛАДНО, КУПЛЮ ВСЕ САМА!''',
        '''На Новый год буду аналитиком! Буду следить: а у всех ли налито?''',
        '''- А ты кем нарядишься на Новый год?
- Кем, кем - сугробом! Снежинка из меня никакая!''',
        '''Путём простейшей перестановки букв из Снегурочки может получиться как эпическая Огнесручка, так и абсолютно неполиткорректная Негросучка.
А пожелание С Новым Годом превращается в брутальное Говно с дымом!''',
        '''После празднования Нового года встречаются два приятеля:
- Ну, как встретил праздник?
- Да не знаю, еще не рассказывали...''',
    ]
    return random.choice(jokes)
