from django.urls import path
from .views import UserViewSet, CustomObtainPairView
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework import permissions


schema_view = get_schema_view(
    openapi.Info(
        title="CustomUser API",
        default_version='v1',
        description="API documentation for managing User instances",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="contact@fobework.com"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=[permissions.AllowAny]
)


urlpatterns = [

    path('api/authentication/login/', CustomObtainPairView.as_view(), name='login'),
    path('api/users/', UserViewSet.as_view({'post': 'create', 'get': 'list'}, name='create-users-list')),
    path('api/users/<int:pk>', UserViewSet.as_view({'get': 'retrieve','delete': 'destroy'}, name='destroy-users-detail')),

    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]
