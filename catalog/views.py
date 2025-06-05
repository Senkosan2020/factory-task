from django.shortcuts import render, redirect
from django.contrib.auth.hashers import check_password
from .models import Master, Worker, Box

def index(request):
    context = {
        'masters_count': Master.objects.count(),
        'workers_count': Worker.objects.count(),
        'boxes_count': Box.objects.count(),
    }
    return render(request, "factory/index.html", context)


def worker_login(request):
    error = None
    if request.method == 'POST':
        wid = request.POST.get('worker_id')
        pwd = request.POST.get('password')
        try:
            worker = Worker.objects.get(worker_id=wid)
        except Worker.DoesNotExist:
            error = 'Invalid ID or password'
        else:
            if check_password(pwd, worker.password):
                request.session['worker_pk'] = worker.pk
                return redirect('index')
            else:
                error = 'Invalid ID or password'
    return render(request, 'registration/login.html', {
        'error': error
    })


def worker_logout(request):
    request.session.pop('worker_pk', None)
    return redirect('index')


def profile(request):
    worker_pk = request.session.get("worker_pk")
    if not worker_pk:
        return redirect("login")
    try:
        worker = Worker.objects.get(pk=worker_pk)
    except Worker.DoesNotExist:
        return redirect("login")

    return render(request, "factory/profile.html", {"worker": worker})


def toggle_at_work(request):
    if request.method != "POST":
        return redirect("profile")

    worker_pk = request.session.get("worker_pk")
    if not worker_pk:
        return redirect("login")

    try:
        worker = Worker.objects.get(pk=worker_pk)
    except Worker.DoesNotExist:
        return redirect("login")

    worker.at_work = not worker.at_work
    worker.save(update_fields=["at_work"])

    return redirect("profile")
