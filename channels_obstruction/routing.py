from channels.routing import ProtocolTypeRouter, URLRouter
from django.urls import path
from channels.auth import AuthMiddlewareStack

from game.consumers import LobbyConsumer, GameConsumer

application = ProtocolTypeRouter({
    # Empty for now (http->django views is added by default)

    "websocket": AuthMiddlewareStack(
        URLRouter([
            # URLRouter just takes standard Django path() or url() entries.
            path("lobby/", LobbyConsumer),
            path("game/<int:game_id>/", GameConsumer)
        ])
    ),

})
