from rest_framework import serializers
from models import SantaUser


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = SantaUser
        fields = ('username', 'email', 'wish')

