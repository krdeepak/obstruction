import re
import logging
import json

from .models import Game, GameSquare
# from channels.auth import channel_session_user
from asgiref.sync import async_to_sync

from .serializers import GameSerializer

from channels.generic.websocket import JsonWebsocketConsumer
log = logging.getLogger(__name__)


class LobbyConsumer(JsonWebsocketConsumer):

    # Set to True to automatically port users from HTTP cookies
    # (you don't need channel_session_user, this implies it)
    http_user = True

    '''
    def connection_groups(self, **kwargs):
        """
        Called to return the list of groups to automatically add/remove
        this connection to/from.
        """
        return ["lobby"]
    '''

    def connect(self):
        """
        Perform things on connection start
        """
        self.accept()
        print('channel name: ', self.channel_name)
        async_to_sync(self.channel_layer.group_add)(
            "lobby",
            self.channel_name,
        )
        print('added channel to group')
        self.send_json({"accept": True})

    def receive_json(self, content, **kwargs):
        """
        Called when a message is received with either text or bytes
        filled out.
        """
        """
        Called when a message is received with either text or bytes
        filled out.
        """

        username = self.scope["user"]
        print(type(username))
        print('content', content)
        print('username', username)
        print('scope', self.scope)

        # get the action that's coming in
        action = content['action']
        if action == 'create_game':
            # create a new game using the part of the channel name
            Game.create_new(username)
            avail_game_list = Game.get_available_games()
            avail_serializer = GameSerializer(avail_game_list, many=True)

            print('sending game info to group')
            print(avail_serializer.data)
            async_to_sync(self.channel_layer.group_send)(
                'lobby',
                {'type': 'game.message', 'text': json.dumps(avail_serializer.data)})

    def disconnect(self, code):
        """
        Perform things on connection close
        """
        pass

    def game_message(self, event):
        print('inside game message')
        print(event)
        self.send_json(json.loads(event['text']))


class GameConsumer(JsonWebsocketConsumer):
    # Set to True to automatically port users from HTTP cookies
    # (you don't need channel_session_user, this implies it)
    http_user = True

    def connection_groups(self, **kwargs):
        """
        Called to return the list of groups to automatically add/remove
        this connection to/from.
        """
        # this sets the game group name, so we can communicate directly with
        # those channels in the game
        # return ["game-{0}".format(kwargs['game_id'])]

    def connect(self):
        """
        Perform things on connection start
        """
        self.accept()
        game_id = self.scope['url_route']['kwargs']['game_id']
        async_to_sync(self.channel_layer.group_add)(
            "game-{0}".format(game_id),
            self.channel_name,
        )
        self.send_json({"accept": True})
        pass

    def receive_json(self, content, **kwargs):
        """
        Called when a message is received with either text or bytes
        filled out.
        """
        # include the Django user in the request
        # channel_session_user = True
        action = content['action']
        user = self.scope["user"]
        print(action)
        print(user)

        # handle based on the specific action called
        if action == 'claim_square':
            # get the square object
            square = GameSquare.get_by_id(content['square_id'])
            # claim it for the user
            square.claim('Selected', user)
            game_id = self.scope['url_route']['kwargs']['game_id']
            game = Game.get_by_id(game_id)
            game.send_game_update()

        if action == 'chat_text_entered':
            # chat text
            game = Game.get_by_id(content['game_id'])
            game.add_log(content['text'], user)
            game.send_game_update()

    def disconnect(self, message, **kwargs):
        """
        Perform things on connection close
        """

    def game_update(self, event):
        print('inside game update')
        print(event)
        self.send_json(json.loads(event['text']))


