from django import urls

from recommend import views

urlpatterns = [
    urls.path("", views.RecommendView.as_view()),
]
