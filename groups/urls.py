from django.urls import path
from . import views

urlpatterns = [
    path("<u_id>/non_members", views.non_members),
    path("<u_id>/members", views.members),
    path("<u_id>/remove", views.remove_from_group),
    path("<u_id>/add", views.add_to_group),
    path("create", views.create_group),
]
