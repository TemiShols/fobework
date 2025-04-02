from django.urls import path, re_path
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from artist.views import ArtistViewSet

schema_view = get_schema_view(
    openapi.Info(
        title="Artists API",
        default_version='v1',
        description="API for managing artist profiles",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="contact@fobework.com"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=[permissions.AllowAny],
)

urlpatterns = [
    path('api/artist/', ArtistViewSet.as_view({
        'get': 'list',
        'post': 'create'
    }), name='artist-list-create'),

    path('api/artist/<int:pk>/', ArtistViewSet.as_view({
        'get': 'retrieve',
        'put': 'update',
        'delete': 'destroy'
    }), name='artist-detail'),

    path('api/artist/<int:pk>/my_profile/', ArtistViewSet.as_view({
        'get': 'my_profile'
    }), name='artist-my-profile'),

    path('api/artist/<int:pk>/verify/', ArtistViewSet.as_view({
        'post': 'verify'
    }), name='artist-verify'),

    re_path(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    re_path(r'^swagger/$', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    re_path(r'^redoc/$', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]