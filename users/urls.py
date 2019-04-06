from rest_framework.authtoken import views as rest_views
from django.urls import path

from . import views

urlpatterns = [
    path("groups", views.created_groups),
    path("inbox", views.inbox),
    path("search/", views.user_search),
    path("login", rest_views.obtain_auth_token),
    path("signup", views.signup),
]
