from django.urls import path
from . import views

urlpatterns = [
    path("<u_id>/add", views.add_to_group),
    path("create", views.create_group),
]
