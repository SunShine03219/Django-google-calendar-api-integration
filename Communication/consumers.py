import json
from channels.generic.websocket import AsyncJsonWebsocketConsumer
from channels.db                import database_sync_to_async
from asgiref.sync               import sync_to_async
from .models                    import *
from django.contrib.auth.models import User


class ChatConsumer(AsyncJsonWebsocketConsumer):
    
    async def connect(self):
        self.room_name          = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name    = "chat_%s" % self.room_name
        self.username           = self.scope['user'].username
        self.user               = await database_sync_to_async(User.objects.get)(username=self.username)
        self.room               = await database_sync_to_async(Room.objects.get)(slug=self.room_name)
        self.room_user1         = await database_sync_to_async(lambda: self.room.user1)()
        self.room_user2         = await database_sync_to_async(lambda: self.room.user2)()
        
        await self.removeNotification()
        
        await self.channel_layer.group_add(self.room_group_name, self.channel_name)
        await self.accept()
    
    async def disconnect(self,close_code):
        await self.removeNotification()
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

    async def receive(self, text_data):
        await self.removeNotification()
        data        = json.loads(text_data)
        message     = data['message']
        username    = data['username']
        room        = data['room']
        
        await self.save_message(username, room, message)
        
        await self.channel_layer.group_send(
            self.room_group_name,    
            {
                'type': 'chat_message',
                'message': message,
                'username': username,
                'room': room,
            },
        )
        
    async def chat_message(self, event):
        await self.removeNotification()
        try:
            message     = event['message']
            username    = event['username']
            room        = event['room']
            await self.send(text_data=json.dumps(
                {
                    'message': message,
                    'username': username,
                    'room': room,    
                }
            ))          
        except Exception as e:
            print(e)
            
    @sync_to_async
    def save_message(self, username, room, message):
        user            = User.objects.get(username=username)
        room            = Room.objects.get(slug=room)
        message         = Message.objects.create(user=user, room=room, content=message)
        notification    = Notification(target=message)
        
        if user == room.user1:
            notification.recipient=room.user2
            notification.actor=room.user1 
            notification.verb = str(notification.actor.company.company) + ' send you a message!'
            
        else:
            notification.recipient=room.user1
            notification.actor=room.user2 
            notification.verb = str(notification.actor.company.company) + ' send you a message!'
        
        if not Notification.objects.filter(recipient=notification.recipient, actor=notification.actor, is_read=False):
            notification.save()  
        
    @sync_to_async    
    def removeNotification(self):
        if str(self.username) == str(self.room_user1):
            notif = Notification.objects.filter(actor = self.room_user2, recipient=self.room_user1)
            notif.delete()  
        else:
            notif = Notification.objects.filter(actor = self.room_user1, recipient=self.room_user2) 
            notif.delete()
            


# https://channels.readthedocs.io/en/stable/topics/channel_layers.html
# https://channels.readthedocs.io/en/stable/tutorial/part_2.html
# https://buildmedia.readthedocs.org/media/pdf/channels/latest/channels.pdf
# https://www.honeybadger.io/blog/django-channels-websockets-chat/