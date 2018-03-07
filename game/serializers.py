from django.contrib.auth.models import User
from .models import Game, GameSquare, GameLog
from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'groups')


class GameSerializer(serializers.ModelSerializer):
    class Meta:
        model = Game
        fields = ('id', 'winner', 'creator', 'opponent', 'cols',
                  'rows', 'completed', 'created', 'current_turn')
        depth = 1
