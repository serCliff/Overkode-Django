from django.conf.urls import url

from . import views


urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^(?P<room_name>[^/]+)/html/$', views.html, name='html'),
    url(r'^(?P<room_name>[^/]+)/python/$', views.python, name='python'),
    url(r'^(?P<room_name>[^/]+)/javascript/$', views.javascript, name='javascript'),
    url(r'^(?P<room_name>[^/]+)/$', views.room, name='room'),
]
