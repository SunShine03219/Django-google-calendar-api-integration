from django.urls import path,re_path

from Communication import consumers
from channels.routing import ProtocolTypeRouter, URLRouter


websocket_urlpatterns = [
    
    re_path(r'ws/chat/(?P<room_name>\w+)/$', consumers.ChatConsumer.as_asgi()),
]

channel_routing = ProtocolTypeRouter({
    "websocket": URLRouter(
        websocket_urlpatterns
    ),
})