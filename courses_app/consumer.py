# import json
# from chat.models import ChatMessage
# from myapp.models import UserProfile
# from mentorapp.models import MentorProfile
# from channels.generic.websocket import AsyncWebsocketConsumer
# from asgiref.sync import sync_to_async

# class ChatConsumer(AsyncWebsocketConsumer):
#     async def connect(self):
#         self.room_name = 'chat_room'
#         self.room_group_name = f'chat_{self.room_name}'

#         #  room group lekk join
#         await self.channel_layer.group_add(
#             self.room_group_name,
#             self.channel_name
#         )

#         # Accept the WebSocket connection
#         await self.accept()

#     async def disconnect(self, close_code):
#         # Leave room group
#         await self.channel_layer.group_discard(
#             self.room_group_name,
#             self.channel_name
#         )

#     async def receive(self, text_data):
#         try:
#             # Parse the received JSON data
#             text_data_json = json.loads(text_data)
#             print(text_data,"rext")
#             message = text_data_json['message']
#             print(message,"message")
#             sender_type = text_data_json['sender_type']
#             print(sender_type,"rext")
#             sender_id = text_data_json['sender_id']
#             receiver_type = text_data_json['receiver_type']
#             receiver_id = text_data_json['receiver_id']
#         except json.JSONDecodeError:
#             await self.send_error_message("Invalid JSON format")
#             return
#         except KeyError as e:
#             await self.send_error_message(f"Missing key in JSON data: {e}")
#             return

       
#         await self.save_message_to_database(message, sender_type, sender_id, receiver_type, receiver_id)

#         # room group ilekk msg snd
#         await self.channel_layer.group_send(
#             self.room_group_name,
#             {
#                 'type': 'chat_message',
#                 'message': message,
#                 'sender_type': sender_type,
#                 'sender_id': sender_id,
#                 'receiver_type': receiver_type,
#                 'receiver_id': receiver_id,
#             }
#         )

#     async def chat_message(self, event):
#         # Send message to WebSocket
#         await self.send(text_data=json.dumps(event))

#     @sync_to_async
#     def save_message_to_database(self, message, sender_type, sender_id, receiver_type, receiver_id):
#         try:
#             # Check if the sender and receiver exist
#             sender_profile = UserProfile.objects.get(id=sender_id)
#             receiver_profile = MentorProfile.objects.get(id=receiver_id)
#         except :
          
#             return
#         ChatMessage.objects.create(
#             sender_type=sender_type,
#             sender=sender_profile,
#             receiver_type=receiver_type,
#             receiver=receiver_profile,
#             message=message
#         )

#         print(ChatMessage,"hllllllllllllllllllllllllllllllll")

#     async def send_error_message(self, error_message):
#         await self.send(text_data=json.dumps({
#             'error': error_message
#         }))

# consumers.py

import json
from channels.generic.websocket import AsyncWebsocketConsumer
from django.shortcuts import get_object_or_404
from .models import Course
from user_app.models import User
from courses_app.models import ChatMessage 

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = 'chat_room'
        self.room_group_name = f'chat_{self.room_name}'

        #  room group lekk join
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        # Accept the WebSocket connection
        await self.accept()

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )
    async def connecting(self):
        self.course_id = self.scope['url_route']['kwargs']['course_id']
        self.course = get_object_or_404(Course, id=self.course_id)
        self.room_group_name = f'course_{self.course_id}_chat'
        self.user = self.scope['user']

        if not self.user.is_authenticated:
            await self.close()
            return

        if self.user != self.course.author and not self.course.students.filter(id=self.user.id).exists():
            await self.close()
            return

        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnecting(self, close_code):
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        await self.save_message(message)

        # Send message to the room group
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message,
            }
        )

    async def chat_message(self, event):
        await self.send(text_data=json.dumps(event))

    async def save_message(self, message):
        # Check if the user has a profile (adjust as necessary)
        if hasattr(self.user, 'profile'):  # or check another condition
            sender = self.user
            receiver = self.course.author  
        else:
            sender = self.course.author
            receiver = self.user

        # Save the message to the database
        ChatMessage.objects.create(
            course=self.course,
            sender=sender,
            receiver=receiver,
            message=message
        )
