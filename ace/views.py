from django.shortcuts import render
from django.utils.safestring import mark_safe
import json


def index(request):
    return render(request, 'ace/index.html', {})
    
def room(request, room_name):
    return render(request, 'ace/room.html', {
        'room_name_json': mark_safe(json.dumps(room_name))
    }) 

    
def javascript(request, room_name):
    return render(request, 'ace/javascript.html', {
        'room_name_json': mark_safe(json.dumps(room_name))
    }) 

    
def python(request, room_name):
    return render(request, 'ace/python.html', {
        'room_name_json': mark_safe(json.dumps(room_name))
    }) 

    
def html(request, room_name):
    return render(request, 'ace/html.html', {
        'room_name_json': mark_safe(json.dumps(room_name))
    }) 

