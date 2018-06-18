from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
# import chat.routing
# import codemirror.routing
import ace.routing

application = ProtocolTypeRouter({
    # (http->django views is added by default)
    'websocket': AuthMiddlewareStack(
        URLRouter(
            ace.routing.websocket_urlpatterns
            # codemirror.routing.websocket_urlpatterns,
            

        )
    ),
})
