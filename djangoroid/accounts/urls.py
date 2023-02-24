from django import urls

from accounts import views

urlpatterns = [
    urls.path("signup/", views.signup),
    urls.path("login/", views.login),
    urls.path("logout/", views.logout),
]
