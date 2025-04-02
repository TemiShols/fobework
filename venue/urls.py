from django.urls import path, re_path
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from .views import VenueViewSet

schema_view = get_schema_view(
    openapi.Info(
        title="Venues API",
        default_version='v1',
        description="API for managing venues",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="contact@fobework.com"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=[permissions.AllowAny],
)

urlpatterns = [
    path('api/venues/', VenueViewSet.as_view({
        'get': 'list',
        'post': 'create'
    }), name='venue-list-create'),

    path('api/venues/<int:pk>/', VenueViewSet.as_view({
        'get': 'retrieve',
        'put': 'update',
        'patch': 'partial_update',
        'delete': 'destroy'
    }), name='venue-detail'),

    re_path(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    re_path(r'^swagger/$', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    re_path(r'^redoc/$', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]