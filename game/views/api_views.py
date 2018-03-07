from rest_framework.views import APIView
from rest_framework import viewsets
from game.serializers import *
from rest_framework.response import Response
from game.models import *

from django.utils.decorators import method_decorator

from django.views.decorators.csrf import csrf_exempt

from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from django.http import Http404


@method_decorator(csrf_exempt, name='dispatch')
class CurrentUserView(APIView):

    def get(self, request):
        serializer = UserSerializer(request.user)
        return Response(serializer.data)


class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer


class PlayerGameViewSet(viewsets.ViewSet):
    """
    API endpoint for player games
    """

    def list(self, request):
        queryset = Game.get_games_for_player(self.request.user)
        serializer = GameSerializer(
            queryset, many=True, context={'request': request})
        return Response(serializer.data)


class AvailableGameViewSet(viewsets.ViewSet):
    """
    API endpoint for available/open games
    """

    def list(self, request):
        queryset = Game.get_available_games(request.user)
        serializer = GameSerializer(queryset, many=True)
        return Response(serializer.data)
