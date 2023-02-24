from django import urls

from search import views

# search/
urlpatterns = [
    urls.path("", views.SearchView.as_view()),
]
