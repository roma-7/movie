from django.conf import settings
from django.contrib import admin
from django.urls import include, path
from django.conf.urls.static import static
from django.conf.urls.i18n import i18n_patterns
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

schema_view = get_schema_view(
    openapi.Info(
        title="Movie",
        default_version='v1',
    ),
    public=True,
)

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("main.urls")),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
]
urlpatterns = [
    *i18n_patterns(*urlpatterns, prefix_default_language=False),
]
