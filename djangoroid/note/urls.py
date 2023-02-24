from django import urls

from note import views

urlpatterns = [
    urls.path("<userPk>/", views.NoteListCreateView.as_view()),
    urls.path("<userPk>/<notePk>/", views.NoteDetailView.as_view()),
    urls.path("<userPk>/<notePk>/fork/", views.fork),
    # urls.path("<userPk>/<notePk>/waffle/", views.TagDestoryView.as_view()),
]