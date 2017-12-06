# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import api_view
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

        if (User.objects.filter(email=data['email']).exists()):
            return Response(status=status.HTTP_300_MULTIPLE_CHOICES)

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
        return play(kwargs['pk'])

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
        'Хей! Если ты читаешь это письмо, то ты был выбран самим Сантой, поздравляю! А теперь шуточка от Санты: \n' + randomJoke() + '\n\nС уважением, гномики',
        '2017.secret.santa.2018@gmail.com',
        [email],
        fail_silently=False,
    )


def play(session_id):
    session = Session.objects.get(pk=session_id)
    if session.alreadyPlayed == 1:
        return Response(status=status.HTTP_409_CONFLICT)

    users = [user for user in session.users.all()]
    random.shuffle(users)
    random.shuffle(users)

    for i, sender in enumerate(users):
        receiver = users[(i + 1) % len(users)]
        print (u"From %s to %s with wish: %s" % (sender.user.email, receiver.user.email, receiver.wish))
        sendPlayEmail(sender.user.email, receiver.user.first_name, receiver.wish)

    session.alreadyPlayed = 1
    session.save()
    return Response(status=status.HTTP_200_OK)


def sendPlayEmail(fromMe, toHim, wish):
    text = 'Хей!\n\nМы определили твою судьбу, ' \
           'адресат твоего подарочка: %s. Да смотри не облажайся! Он хочет: %s\n\nС уважением, гномики.' % (toHim, wish)

    send_mail(
        'Тайный Санта',
        text,
        '2017.secret.santa.2018@gmail.com',
        [fromMe],
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

        '''- А ты кем нарядишься на Новый год?
- Кем, кем - сугробом! Снежинка из меня никакая!''',
        '''Путём простейшей перестановки букв из Снегурочки может получиться как эпическая Огнесручка, так и абсолютно неполиткорректная Негросучка.
А пожелание С Новым Годом превращается в брутальное Говно с дымом!''',
        '''После празднования Нового года встречаются два приятеля:
- Ну, как встретил праздник?
- Да не знаю, еще не рассказывали...''',
        '''В компании встречают Новый год.
         За три минуты до наступления праздника выключают свет, чтобы каждый мог сделать то,
          о чем мечтал целый год. Виктор поцеловал Лену, о которой мечтал еще со школы. 
          Петр погладил по ножке прекрасную Светлану. Андрей погладил грудь Валентины. 
          Изя успел съесть всю икру, которая стояла на столе.''',
        '''Мои родители долго думали, что положить мне под елку. В итоге легли сами. Так появился мой братик.''',
        '''Шел восьмой день Нового года. Хотелось чаю и немножко сдохнуть.''',
        '''По старинной традиции после встречи Нового года в кошельках большинства россиян остаются только отпечатки пальцев.''',
        '''— А мне Наташа на Новый год секс подарила!   — Какая она у тебя неоригинальная всем дарит одно и тоже!''',
        '''У меня в записной книжке телефона давно, не помню как, появилась странная запись под именем "Ад." 
        звонить туда боюсь, но иногда от туда поздравляют с новым годом и днем рождения.''',
        '''— Вовочка, скажи, кто приходит к тебе на Новый год — бородатый, в красной шубе?  — Дедушка Мороз! 
         — Правильно, Вовочка! А кто еще с ним приходит?  Вовочка молчит.  — Ну, Вовочка, ну кто эта девушка с косой?  — Смерть?''',
        '''— Почему евреи празднуют Новый год осенью? — Осенью ёлки дешёвые.''',
        '''Почему в Израиле никогда нет фейерверков на новый год. 
        Зачем покупать фейерверки, когда можно посмотреть, как другие запускают их, подумал каждый.''',
        '''Молодая семья отмечает Новый год. Один из гостей задает вопрос:
          — А кто у вас дома хозяин?  Жена:  — Хозяин, подай голос!  Муж (жалобно):  — Гав!..''',
        '''Зять теще:  — Мама, давайте встретим этот Новый год вместе, все таки следующий год ваш, год Змеи...  
        — Конечно , сынок, а то когда еще соберемся вместе Новый год встречать, года только через три...  
        — А что у нас через три года?  — Год Барана!!!''',
        '''Лето.Тюремная камера. Один зек стучится к другому:  — Вася проснись, с НОВЫМ ГОДОМ тебя! 
         — Ты что сдурел , лето за окном, какой новый год?  — Я только что с допроса — тебе следователь год накинул! '''

    ]
    return random.choice(jokes)
