"""channels_obstruction URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path

from game.views import *
from django.contrib.auth.views import login, logout

from rest_framework.routers import DefaultRouter

urlpatterns = [
    path('admin/', admin.site.urls),
    path('register/', CreateUserView.as_view()),
    path('login/', login, {'template_name': 'login.html'}),
    path('logout/', logout, {'next_page': '/'}),
    path('lobby/', LobbyView.as_view()),
    path('game/<int:game_id>/', GameView.as_view()),

    path('', HomeView.as_view())
]

# urls for api - django rest framework
urlpatterns += [
 path('current-user/', CurrentUserView.as_view()),
 path('game-from-id/<int:game_id>/', SingleGameViewSet.as_view()),

]

router = DefaultRouter()
router.register(r'player-games', PlayerGameViewSet, 'player_games')
router.register(r'available-games', AvailableGameViewSet, 'available_games')
router.register(r'game-squares', GameSquaresViewSet, 'game_squares')
urlpatterns += router.urls
