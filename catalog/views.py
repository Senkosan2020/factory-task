from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.hashers import check_password
from django.views import View
from django.views.generic import TemplateView
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.http import JsonResponse, HttpResponseForbidden
import json

from .models import Master, Worker, Box, Work


class IndexView(TemplateView):
    template_name = "factory/index.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['masters_count'] = Master.objects.count()
        context['workers_count'] = Worker.objects.count()
        context['boxes_count'] = Box.objects.count()
        return context


class WorkerLoginView(View):
    def get(self, request):
        return render(request, 'registration/login.html')

    def post(self, request):
        wid = request.POST.get('worker_id')
        pwd = request.POST.get('password')
        error = None
        try:
            worker = Worker.objects.get(worker_id=wid)
            if check_password(pwd, worker.password):
                request.session['worker_pk'] = worker.pk
                return redirect('index')
            else:
                error = 'Invalid ID or password'
        except Worker.DoesNotExist:
            error = 'Invalid ID or password'

        return render(request, 'registration/login.html', {'error': error})


class WorkerLogoutView(View):
    def get(self, request):
        request.session.pop('worker_pk', None)
        return redirect('index')


class ProfileView(View):
    def get(self, request):
        worker_pk = request.session.get("worker_pk")
        if not worker_pk:
            return redirect("login")

        try:
            worker = Worker.objects.get(pk=worker_pk)
        except Worker.DoesNotExist:
            return redirect("login")

        return render(request, "factory/profile.html", {"worker": worker})


class ToggleAtWorkView(View):
    def post(self, request):
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

    def get(self, request):
        return redirect("profile")


@method_decorator(csrf_exempt, name='dispatch')
class AddWorkView(View):
    def post(self, request):
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

    def get(self, request):
        return JsonResponse({"success": False, "error": "Invalid request"})


class GetWorkTypeView(View):
    def get(self, request):
        work_id = request.GET.get("id_work")
        worker_pk = request.session.get("worker_pk")
        if not worker_pk:
            return redirect("login")

        try:
            work = Work.objects.get(pk=work_id)
            return JsonResponse({"success": True, "type": work.specialization.specialization})
        except Work.DoesNotExist:
            return JsonResponse({"success": False})


class WorkDetailView(View):
    def get(self, request, pk):
        work = get_object_or_404(Work, pk=pk)
        worker_pk = request.session.get("worker_pk")
        if not worker_pk:
            return redirect("login")

        worker = get_object_or_404(Worker, pk=worker_pk)
        return render(request, "factory/work_detail.html", {"work": work, "worker": worker})


class RemoveAndReadyView(View):
    def post(self, request, pk):
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

    def get(self, request, pk):
        return redirect("work_detail", pk=pk)


class RemoveOnlyView(View):
    def post(self, request, pk):
        worker_pk = request.session.get("worker_pk")
        if not worker_pk:
            return redirect("login")

        worker = get_object_or_404(Worker, pk=worker_pk)
        work = get_object_or_404(Work, pk=pk)

        if work in worker.works.all():
            worker.works.remove(work)
            return redirect("profile")

        return HttpResponseForbidden("You cannot modify this work.")

    def get(self, request, pk):
        return redirect("work_detail", pk=pk)


class SomeView(View):
    def get(self, request):
        worker = get_object_or_404(Worker, worker_id="some_id_from_context")
        worker_pk = request.session.get("worker_pk")
        if not worker_pk:
            return redirect("login")

        return render(request, "factory/profile.html", {"worker": worker})
