from django.urls import path
from . import views

urlpatterns = [
    path("<u_id>/unfavorite", views.unfavorite_post),
    path("<u_id>/favorite", views.favorite_post),
    path("upload_photo", views.upload_photo),
]
