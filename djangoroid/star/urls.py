from django import urls
from django.contrib import auth
from django.contrib.auth import views as auth_views

from star import views

urlpatterns = [
    urls.path("<userPk>/<notePk>/waffle/", views.note_waffle_view),
    urls.path("<userPk>/<notePk>/comment/<commentPK>/waffle/", views.comment_waffle_view),
]
