from channels.routing import ProtocolTypeRouter, URLRouter
from django.urls import path

from game.consumers import LobbyConsumer

application = ProtocolTypeRouter({
    # Empty for now (http->django views is added by default)

    "websocket": URLRouter([
            # URLRouter just takes standard Django path() or url() entries.
            path("lobby/", LobbyConsumer),
        ]),

})
