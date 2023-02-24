from django import urls
from django.contrib import auth
from django.contrib.auth import views as auth_views

from accounts import views

urlpatterns = [
    urls.path("signup/", views.signup),
    urls.path("login/", views.login),
    urls.path("logout/", views.logout),
    urls.path("profile/", views.ProfileView.as_view()),
]
