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
from catalog.views import (
    IndexView,
    WorkerLoginView,
    WorkerLogoutView,
    ProfileView,
    ToggleAtWorkView,
    AddWorkView,
    GetWorkTypeView,
    WorkDetailView,
    RemoveAndReadyView,
    RemoveOnlyView,
    SomeView
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', IndexView.as_view(), name='index'),
    path('accounts/login/', WorkerLoginView.as_view(), name='login'),
    path('accounts/logout/', WorkerLogoutView.as_view(), name='logout'),
    path("profile/", ProfileView.as_view(), name="profile"),
    path("profile/toggle/", ToggleAtWorkView.as_view(), name="toggle_at_work"),
    path("add-work/", AddWorkView.as_view(), name="add_work"),
    path("get-work-type/", GetWorkTypeView.as_view(), name="get_work_type"),
    path("work/<str:pk>/detail/", WorkDetailView.as_view(), name="work_detail"),
    path("work/<str:pk>/remove_and_ready/", RemoveAndReadyView.as_view(), name="remove_and_ready"),
    path("work/<str:pk>/remove_only/", RemoveOnlyView.as_view(), name="remove_only"),
    path("some/", SomeView.as_view(), name="some_view"),
]
