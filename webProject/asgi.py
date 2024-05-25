"""
ASGI config for webProject project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/howto/deployment/asgi/
"""

#application = get_asgi_application()

import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'webProject.settings')
django.setup()

from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
from channels.sessions import SessionMiddlewareStack
import mainApp.routing

#os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'webProject.settings')


application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    # Добавьте URLRouter для обработки WebSocket
    "websocket": SessionMiddlewareStack(
        URLRouter(
            mainApp.routing.websocket_urlpatterns
        )
    ),
    "ws":AuthMiddlewareStack(
        URLRouter(
            mainApp.routing.websocket_urlpatterns
        )
    ),
})


