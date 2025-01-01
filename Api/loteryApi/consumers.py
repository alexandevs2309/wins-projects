import json
from channels.generic.websocket import AsyncWebsocketConsumer

class LotteryConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = 'lottery_room'
        self.room_group_name = 'lottery_group'
     
     # Unir al grupo de WebSocket
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
       # Salir del grupo de WebSocket
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    # Recibir mensaje del WebSocket
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']

       # Enviar mensaje al grupo de WebSocket
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message
            }
        )

    # Recibir mensaje del grupo de WebSocket
    async def chat_message(self, event):
        message = event['message']

       # Enviar mensaje al WebSocket
        await self.send(text_data=json.dumps({
            'message': message
        }))