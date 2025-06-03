"""
ASGI config for core project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/howto/deployment/asgi/
"""

import os

from channels.routing import ProtocolTypeRouter
from channels.routing import URLRouter
from django.core.asgi import get_asgi_application

asgi_application = get_asgi_application()

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "core.settings")

from apps.websocket.urls import websocket_urlpatterns  # noqa

from apps.shared.middlewares.websocket import JWTAuthMiddleware  # noqa

application = ProtocolTypeRouter(
    {
        "http": asgi_application,
        "websocket": JWTAuthMiddleware(URLRouter(websocket_urlpatterns)),
    }
)
