from channels.generic.websocket import AsyncWebsocketConsumer
import json
# from random import randint
 


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = 'chat_%s' % self.room_name
        self.user_id = False
        self.port = self.scope['client'][1]
        self.username = self.scope['user'] #TODO: Recoger bien el username
        self.username = "Anonymous"

        print("\n\n-------------------------------------------------------------------")
        print("-----------------------  ROOM - "+str(self.room_name)+"  -----------------------------")
        print("-------------------------------------------------------------------")
        print("New User: "+str(self.username))
        print("Connecting...\n")

        # print("\nFAKE LOG")
        # Join room group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()


    async def disconnect(self, close_code):
        # Leave room group
        # print("Bye\n")
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    # Receive message from WebSocket
    async def receive(self, text_data):
        message = json.loads(text_data)


        if not self.user_id:
            self.user_id = str(message['creation']['user'])
            message['receivers'][self.user_id]['port'] = self.port

        print("\nReceive ("+str(self.user_id)+")")
        print(message)

        # Send message to room group
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message,
            }
        )


    # Receive message from room group
    async def chat_message(self, event):
        message = event['message']

        new_receiver = dict()
        new_receiver['id'] = self.user_id        
        new_receiver['username'] = self.username
        new_receiver['port'] = self.port
        message['sent_by'] = new_receiver

        print("\nchat_message ("+str(self.user_id)+")")
        print(event)


        # if not self.user_id in message['receivers']:
            # Send message to WebSocket
        # message = self.add_receiver(message)
        await self.send(text_data=json.dumps(message))




    def add_receiver(self, message):
        """ Add a new receiver of message to not send another time """
        print("")
        print("add_receiver")
        new_receiver = dict()
        new_receiver['id'] = self.user_id        
        new_receiver['username'] = self.username
        new_receiver['port'] = self.port
        print (new_receiver)
        # message['receivers'][self.user_id] = new_receiver

        return message





class User:

    def __init__(self, id, username, port):
        self.id = id
        self.username = username
        self.port = port



