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
        self.reply_code = False


        # print("\nFAKE LOG")
        # Join room group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        print("\n\n-------------------------------------------------------------------")
        print("-----------------------  ROOM -- "+str(self.room_name)+"  -----------------------------")
        print("-------------------------------------------------------------------")
        await self.accept()
        print("New User: "+str(self.username))
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
        action = message['creation']['action']
        
        message['sent_by'] = self.user_id

        if 'content' in message:
            content = hash(str(message['content']))

        if action == "connecting":
            #TODO: Saber si eres el primero
            self.user_id = str(message['creation']['user'])
            print("Conected ["+self.user_id+"]\n")
            # Initial text request
            await self.group_send_m({'sent_by': self.user_id, 'creation': {'action': 'fetch_code'}})
        
        elif action == "reply_code":
            print("\n------------------------------------------")
            print("["+self.user_id+"] Reply code: ")
            print(message)
            self.reply_code = True
            await self.group_send_m(message)


        else:
            print("\n------------------------------------------")
            print("["+self.user_id+"] Sending message:")
            print(message)
            
            if not self.check_received(content):
                await self.group_send_m(message)
            


    # Receive message from room group
    async def chat_message(self, event):
        message = event['message']
        action = message['creation']['action']

        print("\n["+self.user_id+"] Received message by: ("+str(message['sent_by'])+") Action: "+str(message['creation']['action']).upper())
        print(event)
        
        if 'content' in message:
            content = hash(str(message['content']))

        if action == "fetch_code":
            #Request the text to his editor
            if self.user_id != message['sent_by']:
                # Only me need the initial code reception
                print("Envio mensaje FETCH CODE al editor para recoger contenido inicial")
                print("Espero reply para enviar a todos")
                await self.send(text_data=json.dumps(message))
            else:
                print("Yo no envio mesaje a mi editor porque soy el que lo está pidiendo")


        elif action == "reply_code":
            if self.user_id != message['sent_by'] and not self.reply_code:
                print("Recibo contenido inicial")
                self.reply_code = True
                message['creation']['action'] = "insert"
                message['content']['action'] = "insert"

                self.check_received(hash(str(message['content'])))
                await self.send(text_data=json.dumps(message))
        else:
            # Discard our changes
            if self.user_id != message['sent_by'] and not self.check_received(content): 
                #Send message to our editor
                print("Envio mensaje de actualizacion a mi editor")
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
    

    def check_received(self, content):
        # Si nunca he recibido un mensaje igual, lo pongo a false y lo envio esperando replica
        # Si lo he recibido:
        # - Si está a false, lo pongo a True, ES LA RÉPLICA
        # - Si esta a true, se ha generado un mensaje idéntico, lo pongo a false y lo envio esperando replica
        

        if not content in self.received_messages:
            print("** Mensaje nuevo **")
            self.received_messages[content] = False
        else:
            if self.received_messages[content]:
                print("** Mensaje repetido, envio de nuevo **")
                self.received_messages[content] = False
            else:
                print("** Replica recibida **")
                self.received_messages[content] = True

        return self.received_messages[content]
            

