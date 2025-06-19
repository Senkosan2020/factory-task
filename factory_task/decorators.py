from django.shortcuts import redirect
from functools import wraps

def worker_login_required(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if not request.session.get("worker_id"):
            return redirect("login")
        return view_func(request, *args, **kwargs)
    return wrapper