from django import urls

from note import views as note_views

urlpatterns = [
    urls.path("<int:uid>/", note_views.NoteListCreateView.as_view()),
    urls.path("<int:uid>/<int:nid>", note_views.NoteRetrieveUpdateDestroyView.as_view()),
    urls.path("<int:uid>/<int:nid>/fork/", note_views.NoteForkCreateView.as_view()),
    urls.path("<int:uid>/<int:nid>/waffle/", note_views.WaffleListCreateView.as_view()),
    urls.path("<int:uid>/<int:nid>/comment/", note_views.CommentListCreateView.as_view()),
    urls.path("<int:uid>/<int:nid>/comment/<int:cid>/", note_views.CommentRetrieveUpdateDestroyView.as_view()),
]
