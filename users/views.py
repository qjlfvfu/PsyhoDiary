from django.shortcuts import render
from django.views import generic
from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView

from .serializers import (
    MyTokenObtainPairSerializer,
    UserDetailSerializer, UserSerializer,
    UserCreateSerializer,
)
from .models import CustomUser

# Create your views here.
User = CustomUser  # или get_user_model()


class MyTokenObtainPairView(TokenObtainPairView):
    """Получение Токена"""
    serializer_class = MyTokenObtainPairSerializer


# =============== CRUD User =================
class UserListAPIView(generics.ListAPIView):
    """Список пользователей"""
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        if self.request.user.is_staff:
            return User.objects.all()
        return User.objects.filter(id=self.request.user.id)


class UserRetrieveAPIView(generics.RetrieveAPIView):
    """Просмотр пользователя"""
    queryset = User.objects.all()
    serializer_class = UserDetailSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user

        if user.groups.filter(name="doctor").exists():
            return User.objects.all()

        if user.is_staff or user.groups.filter(name="moderators").exists():
            return User.objects.all()

    def get_object(self):
        if self.kwargs.get("pk") == "me":
            return self.request.user
        return super().get_object()


class UserCreateAPIView(generics.CreateAPIView):
    """Регистрация нового пользователя"""
    queryset = User.objects.all()
    serializer_class = UserCreateSerializer
    permission_classes = [AllowAny]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()

        refresh = RefreshToken.for_user(user)

        return Response(
            {
                'user': UserSerializer(user).data,
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            },
            status=status.HTTP_201_CREATED
        )


class UserUpdateAPIView(generics.UpdateAPIView):
    """Обновление информации о пользователе"""
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return User.objects.filter(id=self.request.user.id)


class UserDestroyAPIView(generics.DestroyAPIView):
    """Удаление пользователя"""
    queryset = User.objects.all()
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.is_staff or user.group.filter (name="moderator").exists():
            return User.objects.all()
        return User.objects.filter(id=user.id)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(
            {"message": "Пользователь удален"},
            status=status.HTTP_204_NO_CONTENT,
        )