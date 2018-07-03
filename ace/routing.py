from django.conf.urls import url
from . import consumers


websocket_urlpatterns = [
    url(r'^ws/ace/(?P<room_name>[^/]+)/$', consumers.OverkodeConsumer),
    url(r'^ws/ace/(?P<room_name>[^/]+)/javascript/', consumers.OverkodeConsumer),
    url(r'^ws/ace/(?P<room_name>[^/]+)/python/', consumers.OverkodeConsumer),
    url(r'^ws/ace/(?P<room_name>[^/]+)/html/', consumers.OverkodeConsumer),
]
