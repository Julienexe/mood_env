import json
from django.http import JsonResponse
from channels.generic.websocket import WebsocketConsumer
from asgiref.sync import async_to_sync

from .models import Message
from .views import lobby
from mood_trackers.models import User



class ChatConsumer(WebsocketConsumer):
    def fetch_messages(self, data):
        messages = Message.last_10_messages(self)
        result = str(self.messages_to_json(messages))
        content = {
            'command':'messages',
            'messages': result
        }
        self.send_message(content)

    def new_message(self, data):
        author = data['email']
        author_user = User.objects.get(email = author)
        message = Message.objects.create(
            author=author_user,
            content=data['message']
        )
        content = {
            'command':'new_message',
            'message': self.message_to_json(message)
        }
        return self.send_chat_message(content)

    def messages_to_json(self,messages):
        result=[]
        for message in messages:
            result.append(self.message_to_json(message))
        return result    
    
    def message_to_json(self,message):
        # return JsonResponse(message, safe = False)
        return{
            "author": message.author.name,
            "content": message.content,
            "timestamp": str(message.timestamp),
        }

    commands = {
        'fetch_messages': fetch_messages,
        'new_message': new_message
    }


    def connect(self):
        self.room_name = self.scope["url_route"]["kwargs"]
        self.room_group_name = 'test'

        #joining a group
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name
        )

        self.accept()

    def receive(self, text_data):
        data = json.loads(text_data)
        self.commands[data['command']](self, data)


    def send_chat_message(self, content):    
        #receiving messages from the group
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                "type": "chat_message",
                "message": content
            }
        )

    def send_message(self,content):
        self.send(text_data=json.dumps(content))

    def chat_message(self, event):
        message = event['message']
        
        #sending messages to the group
        self.send(text_data=json.dumps(message))   