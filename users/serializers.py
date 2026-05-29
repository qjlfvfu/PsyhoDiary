from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from .models import CustomUser, DoctorProfile

User = get_user_model()


# ========== JWT ==========
class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    """Кастомный сериализатор для JWT токена"""

    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        # Добавление пользовательских полей в токен
        token["username"] = user.username
        token["email"] = user.email
        token["first_name"] = user.first_name
        token["last_name"] = user.last_name
        token["is_moderator"] = user.groups.filter(name="moderators").exists()
        token["is_doctor"] = user.groups.filter(name="doctor").exists()

        return token


# ========== Базовые сериализаторы пользователя ==========
class UserSerializer(serializers.ModelSerializer):
    """Базовый сериализатор для пользователя"""

    class Meta:
        model = User
        fields = [
            "id",
            "email",
            "first_name",
            "last_name",
            "description",
            "phone_number",
            "avatar",
        ]
        read_only_fields = ["id"]


class UserDetailSerializer(serializers.ModelSerializer):
    """Детальный сериализатор пользователя"""

    is_moderator = serializers.SerializerMethodField()
    is_doctor = serializers.SerializerMethodField()
    full_name = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = [
            "id",
            "email",
            "first_name",
            "last_name",
            "full_name",
            "phone_number",
            "avatar",
            "date_joined",
            "is_moderator",
            "is_doctor",
        ]
        read_only_fields = ["id", "date_joined"]

    def get_is_moderator(self, obj):
        return obj.groups.filter(name="moderators").exists()

    def get_is_doctor(self, obj):
        return obj.groups.filter(name="doctor").exists()

    def get_full_name(self, obj):
        return f"{obj.first_name} {obj.last_name}".strip() or obj.email


class UserCreateSerializer(serializers.ModelSerializer):
    """Сериализатор для регистрации пользователя"""

    password = serializers.CharField(
        write_only=True, required=True, validators=[validate_password]
    )
    password2 = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = [
            "email",
            "password",
            "password2",
            "first_name",
            "last_name",
            "phone_number",
        ]

    def validate(self, attrs):
        if attrs["password"] != attrs["password2"]:
            raise serializers.ValidationError({"password": "Пароли не совпадают"})
        return attrs

    def create(self, validated_data):
        validated_data.pop("password2")
        validated_data["username"] = validated_data["email"].split("@")[0]
        user = User.objects.create_user(**validated_data)
        return user


class UserUpdateSerializer(serializers.ModelSerializer):
    """Сериализатор для обновления профиля"""

    class Meta:
        model = User
        fields = ["first_name", "last_name", "phone_number", "avatar"]


# ========== Профиль пользователя ==========


class PublicUserProfileSerializer(serializers.ModelSerializer):
    """
    Публичный сериализатор для просмотра чужих профилей
    """

    full_name = serializers.SerializerMethodField()

    class Meta:
        model = CustomUser
        fields = ["id", "email", "full_name", "avatar"]

    def get_full_name(self, obj):
        return f"{obj.first_name} {obj.last_name}".strip() or obj.email


class PrivateUserProfileSerializer(serializers.ModelSerializer):
    """
    Приватный сериализатор для просмотра профиля пациента
    """

    full_name = serializers.SerializerMethodField()

    class Meta:
        model = CustomUser
        fields = ["full_name", "phone_number", "avatar", "email", "description"]

    def get_full_name(self, obj):
        return f"{obj.first_name} {obj.last_name}".strip() or obj.email


class DoctorProfileSerializer(serializers.ModelSerializer):
    """Сериализатор для профиля врача"""

    user = UserSerializer(read_only=True)
    full_name = serializers.SerializerMethodField()

    class Meta:
        model = DoctorProfile
        fields = [
            "id",
            "user",
            "full_name",
            "specialization",
            "experience_years",
            "license_number",
        ]

    def get_full_name(self, obj):
        return f"{obj.user.first_name} {obj.user.last_name}".strip() or obj.user.email
