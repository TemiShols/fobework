from .views import BookingViewSet
from django.urls import path
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

schema_view = get_schema_view(
    openapi.Info(
        title="Booking API",
        default_version='v1',
        description="API for managing Bookings",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="contact@fobework.com"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=[permissions.AllowAny],
)

urlpatterns = [
    path('api/bookings/', BookingViewSet.as_view({
        'get': 'list',
        'post': 'create'
    })),
    path('api/bookings/<int:pk>/', BookingViewSet.as_view({
        'get': 'retrieve',
        'put': 'update',
        'delete': 'destroy'
    })),
    path('api/bookings/<int:pk>/receipt/', BookingViewSet.as_view({
        'get': 'receipt'
    })),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]