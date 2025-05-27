from catalog.models import Worker

def current_worker(request):
    worker_pk = request.session.get('worker_pk')
    if not worker_pk:
        return {}
    try:
        worker = Worker.objects.get(pk=worker_pk)
    except Worker.DoesNotExist:
        return {}
    return {'worker': worker}
