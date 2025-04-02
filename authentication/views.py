from drf_yasg import openapi
from .models import CustomUser
from .serializers import CustomUserSerializer
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework import viewsets, status
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from drf_yasg.utils import swagger_auto_schema
from rest_framework_simplejwt.views import TokenObtainPairView
from .serializers import MyTokenObtainPairSerializer


class StandardResultsSetPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100


class UserViewSet(viewsets.ViewSet):
    authentication_classes = []
    permission_classes = [IsAuthenticated]

    def get_permissions(self):
        if self.action == 'create':
            permission_classes = [AllowAny]
        else:
            permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]

    @swagger_auto_schema(
        operation_summary="Create a new user",
        request_body=CustomUserSerializer,
        responses={
            201: CustomUserSerializer,
            400: "Bad Request",
        },
    )
    def create(self, request):
        serializer = CustomUserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @swagger_auto_schema(
        operation_summary="List all users",
        responses={200: CustomUserSerializer(many=True)},
    )
    def list(self, request):
        users = CustomUser.objects.all()
        paginator = StandardResultsSetPagination()
        users = paginator.paginate_queryset(users, request)
        serializer = CustomUserSerializer(users, many=True)
        return paginator.get_paginated_response(serializer.data)

    @swagger_auto_schema(
        operation_summary="Retrieve a single user by ID",
        responses={
            200: CustomUserSerializer,
            404: "User not found",
        },
    )
    def retrieve(self, request, pk=None):
        user = get_object_or_404(CustomUser, id=pk)
        serializer = CustomUserSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        operation_summary="Update an existing user",
        request_body=CustomUserSerializer,
        responses={
            200: CustomUserSerializer,
            400: "Bad Request",
        },
    )
    def update(self, request, pk=None):
        user = get_object_or_404(CustomUser, id=pk)
        serializer = CustomUserSerializer(user, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        operation_summary="Delete a user",
        responses={
            204: "User deleted successfully",
            404: "User not found",
        },
    )
    def destroy(self, request, pk=None):
        user = get_object_or_404(CustomUser, id=pk)
        user.delete()
        return Response({"message": "User deleted successfully"}, status=status.HTTP_204_NO_CONTENT)


class CustomObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer

    @swagger_auto_schema(
        operation_summary="Obtain JWT token pair",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=['email', 'password'],
            properties={
                'email': openapi.Schema(type=openapi.TYPE_STRING, description='User email'),
                'password': openapi.Schema(type=openapi.TYPE_STRING, description='User password'),
            },
        ),
        responses={
            200: openapi.Response(
                description="JWT token pair",
                examples={
                    "application/json": {
                        "refresh": "your_refresh_token",
                        "access": "your_access_token",
                        "user_id": 1,
                        "email": "user@example.com"
                    }
                },
            ),
            400: "Bad Request",
        },
    )
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)