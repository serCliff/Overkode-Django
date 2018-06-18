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
        self.received_messages = dict()

        print("\n\n-------------------------------------------------------------------")
        print("-----------------------  ROOM -- "+str(self.room_name)+"  -----------------------------")
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
        await self.send(text_data=json.dumps({'creation': {'timestamp': 'now', 'action': 'connecting'}}))


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

        if message['creation']['action'] == "connecting":
            self.user_id = str(message['creation']['user'])
            # Enviar mensaje de comunicación para recibir datos de la página
        else:
            message['sent_by'] = self.user_id

            
            print("\n------------------------------------------")
            print("["+self.user_id+"] Sending message:")
            print(message)
            
            content = hash(str(message['content']))
            # import pdb; pdb.set_trace()
            
            # Si nunca he recibido un mensaje igual, lo pongo a false y lo envio esperando replica
            # Si lo he recibido:
            # - Si está a false, lo pongo a True, ES LA RÉPLICA
            # - Si esta a true, se ha generado un mensaje idéntico, lo pongo a false y lo envio esperando replica

            if not content in self.received_messages:
                print("Mensaje nuevo")
                self.received_messages[content] = False
                await self.group_send_m(message)
            else:
                if self.received_messages[content]:
                    print("Mensaje repetido, envio de nuevo")
                    self.received_messages[content] = False
                    await self.group_send_m(message)
                else:
                    print("Replica recibida")
                    self.received_messages[content] = True




            

            


    # Receive message from room group
    async def chat_message(self, event):
        message = event['message']
        content = hash(str(message['content']))

        print("\n["+self.user_id+"] Received message by: ("+str(message['sent_by'])+") Action: "+str(message['creation']['action']).upper())
        print(event)
        # import pdb; pdb.set_trace()

        if not content in self.received_messages:
            print("Mensaje nuevo")
            self.received_messages[content] = False
        else:
            if self.received_messages[content]:
                print("Mensaje repetido, envio de nuevo")
                self.received_messages[content] = False
            else:
                print("Replica recibida")
                self.received_messages[content] = True

        # Discard our changes
        if self.user_id != message['sent_by'] and not self.received_messages[content]: 
            #Send message to our editor
            await self.send(text_data=json.dumps(message))
        

    async def group_send_m(self, message):
        # Send message to room group
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message,
            }
        )


class User:

    def __init__(self, id, username, port):
        self.id = id
        self.username = username
        self.port = port



