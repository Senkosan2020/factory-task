from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.hashers import check_password
from django.contrib.auth.decorators import login_required
from .models import Master, Worker, Box, Work
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse, HttpResponseForbidden
import json
from factory_task.decorators import worker_login_required


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


@csrf_exempt
def add_work(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            work_id = data.get("id_work")
            worker_id = data.get("worker_id")

            if not work_id or not worker_id:
                return JsonResponse({"success": False, "error": "Missing data"})

            work = Work.objects.get(pk=work_id)
            worker = Worker.objects.get(pk=worker_id)

            if work in worker.works.all():
                return JsonResponse({"success": False, "error": "Work already assigned"})

            worker.works.add(work)
            return JsonResponse({"success": True})

        except Work.DoesNotExist:
            return JsonResponse({"success": False, "error": "Work not found"})
        except Worker.DoesNotExist:
            return JsonResponse({"success": False, "error": "Worker not found"})
        except Exception as e:
            return JsonResponse({"success": False, "error": str(e)})

    return JsonResponse({"success": False, "error": "Invalid request"})


def get_work_type(request):
    work_id = request.GET.get("id_work")
    worker_pk = request.session.get("worker_pk")
    if not worker_pk:
        return redirect("login")
    try:
        work = Work.objects.get(pk=work_id)
        return JsonResponse({"success": True, "type": work.specialization.specialization})
    except Work.DoesNotExist:
        return JsonResponse({"success": False})


def work_detail(request, pk):
    work = get_object_or_404(Work, pk=pk)
    worker_pk = request.session.get("worker_pk")
    if not worker_pk:
        return redirect("login")

    worker = get_object_or_404(Worker, pk=worker_pk)
    return render(request, "factory/work_detail.html", {"work": work, "worker": worker})


def remove_and_ready(request, pk):
    if request.method == "POST":
        worker_pk = request.session.get("worker_pk")
        if not worker_pk:
            return redirect("login")

        worker = get_object_or_404(Worker, pk=worker_pk)
        work = get_object_or_404(Work, pk=pk)

        if work in worker.works.all():
            worker.works.remove(work)
            work.ready = True
            work.save()
            return redirect("profile")

        return HttpResponseForbidden("You cannot modify this work.")
    return redirect("work_detail", pk=pk)


def remove_only(request, pk):
    if request.method == "POST":
        worker_pk = request.session.get("worker_pk")
        if not worker_pk:
            return redirect("login")

        worker = get_object_or_404(Worker, pk=worker_pk)
        work = get_object_or_404(Work, pk=pk)

        if work in worker.works.all():
            worker.works.remove(work)
            return redirect("profile")

        return HttpResponseForbidden("You cannot modify this work.")
    return redirect("work_detail", pk=pk)


def some_view(request):
    worker = get_object_or_404(Worker, worker_id="some_id_from_context")
    worker_pk = request.session.get("worker_pk")
    if not worker_pk:
        return redirect("login")
    context = {
        "worker": worker,
    }
    return render(request, "factory/profile.html", context)
