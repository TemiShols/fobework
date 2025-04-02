from django.urls import path, re_path
from .views import EventViewSet
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework import permissions

schema_view = get_schema_view(
    openapi.Info(
        title="Events API",
        default_version='v1',
        description="API documentation for managing Event Booking",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="contact@fobework.com"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=[permissions.AllowAny],
)

urlpatterns = [
    path('api/events/', EventViewSet.as_view({
        'post': 'create',
        'get': 'list'
    }), name='event-list-create'),

    path('api/events/<int:pk>/', EventViewSet.as_view({
        'get': 'retrieve',
        'put': 'update',
        'patch': 'partial_update',
        'delete': 'destroy'
    }), name='event-detail'),

    path('api/events/<int:pk>/artist_events/', EventViewSet.as_view({
        'get': 'artist_events'
    }), name='event-artist-events'),

    re_path(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]