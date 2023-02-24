from django import urls

from comment import views

urlpatterns = [
    urls.path("<userPk>/<notePk>/comment/",
              views.CommentListView.as_view()),
    urls.path("<userPk>/<notePk>/comment/create/",
              views.CommentCreateView.as_view()),
    urls.path("<userPk>/<notePk>/comment/<commentPk>/",
              views.CommentDetailView.as_view()),
    # urls.path("<userPk>/<notePk>/commnet/<commentPk>/waffle/", views.CommentDetailView.as_view()),
]
