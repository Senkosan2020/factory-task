from django.shortcuts import render
from .models import Master, Worker, Box

def index(request):
    context = {
        'masters_count': Master.objects.count(),
        'workers_count': Worker.objects.count(),
        'boxes_count': Box.objects.count(),
    }
    return render(request, "factory/index.html", context)
