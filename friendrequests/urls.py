from django.urls import path
from . import views

urlpatterns = [
    path("<username>", views.send_friend_request),
]
