from django import urls
from django.conf import settings
from rest_framework import permissions

from drf_yasg import openapi
from drf_yasg import views as drf_views

schema_view = drf_views.get_schema_view(
    openapi.Info(
        title="DjangoRoid API",
        default_version="v1",
        description="DjangoRoid API 문서입니다",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="enkeejuniour@snu.ac.kr"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=[permissions.AllowAny],
)

if settings.DEBUG:
    urlpatterns = [
        urls.re_path(r"^swagger(?P<format>\.json|\.yaml)$", schema_view.without_ui(cache_timeout=0), name="schema-json"),
        urls.re_path(r"^swagger/$", schema_view.with_ui("swagger", cache_timeout=0), name="schema-swagger-ui"),
        urls.re_path(r"^redoc/$", schema_view.with_ui("redoc", cache_timeout=0), name="schema-redoc"),
    ]
