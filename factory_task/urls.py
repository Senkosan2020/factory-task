"""
URL configuration for factory_task project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from catalog.views import index, worker_login, worker_logout, profile, toggle_at_work, add_work, get_work_type, work_detail, remove_and_ready, remove_only

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', index, name='index'),
    path('accounts/login/', worker_login, name='login'),
    path('accounts/logout/', worker_logout, name='logout'),
    path("profile/", profile, name="profile"),
    path("profile/toggle/", toggle_at_work, name="toggle_at_work"),
    path("add-work/", add_work, name="add_work"),
    path("get-work-type/", get_work_type, name="get_work_type"),
    path("work/<str:pk>/detail/", work_detail, name="work_detail"),
    path("work/<str:pk>/remove_and_ready/", remove_and_ready, name="remove_and_ready"),
    path("work/<str:pk>/remove_only/", remove_only, name="remove_only"),
]
