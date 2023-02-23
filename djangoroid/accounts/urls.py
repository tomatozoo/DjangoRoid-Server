from django import urls
from django.contrib import auth
from django.contrib.auth import views as auth_views

from accounts import views

urlpatterns = [
    urls.path("signup/", views.signup),
    urls.path("login/", views.login),
    urls.path("logout/", views.logout),
]

# urlpatterns = [
#     urls.path('login/', auth_views.LoginView.as_view(), name='login'),
#     urls.path('logout/', auth_views.LogoutView.as_view(), name='logout'),
# ]