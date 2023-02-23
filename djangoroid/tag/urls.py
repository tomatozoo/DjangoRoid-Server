from django import urls
from django.contrib import auth
from django.contrib.auth import views as auth_views

from tag import views

urlpatterns = [
    urls.path("", views.TagListCreateView.as_view()),
    urls.path("create/", views.TagListCreateView.as_view()),
    urls.path("delete/<tid>/", views.TagDestoryView.as_view()),
]

# urlpatterns = [
#     urls.path('login/', auth_views.LoginView.as_view(), name='login'),
#     urls.path('logout/', auth_views.LogoutView.as_view(), name='logout'),
# ]