from django.urls import path
from .consumer import ChatConsumer

websocket_urlpatterns = [
    path('ws/chat/support/<int:course_id>/', ChatConsumer.as_asgi()),
]
