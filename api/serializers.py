from rest_framework import serializers
from models import SantaUser, Session


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = SantaUser
        fields = '__all__'
        depth = 1


class SessionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Session
        fields = '__all__'
        depth = 2
