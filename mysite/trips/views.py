from django.shortcuts import render

# Create your views here.

# trips/views.py

from datetime import datetime
from django.shortcuts import render


def hello_world(request):
    return render(request, 'hello_world.html', {
        'current_time': str(datetime.now()),
    })
