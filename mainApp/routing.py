from channels.routing import ProtocolTypeRouter, URLRouter
from django.urls import path
from . import consumers


websocket_urlpatterns = [
    path('ws/echo/', consumers.EchoConsumer.as_asgi()),
    path('ws/', consumers.EchoConsumer.as_asgi()),
    path('/echo/', consumers.EchoConsumer.as_asgi()),
    path('', consumers.EchoConsumer.as_asgi()),
]



