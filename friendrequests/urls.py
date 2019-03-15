from django.urls import path
from . import views

urlpatterns = [
    path("<username>", views.send_friend_request),
    path("<username>/accept", views.accept_friend_request),
    path("<username>/delete", views.delete_friend_request),
]
