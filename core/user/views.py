from rest_framework import viewsets, permissions, generics
from .models import MyUser, Email2FACode
from .serializers import (
    MyUserSerializer,
    Email2FACodeSerializer,
    RegisterSerializer,
)
from .permissions import IsAdminOrSelf
import random
from django.core.mail import send_mail
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from .models import MyUser, Email2FACode


# Регистрация
class RegisterView(generics.CreateAPIView):
    queryset = MyUser.objects.all()
    permission_classes = [permissions.AllowAny]  # доступен всем
    serializer_class = RegisterSerializer


# Пользователи
class MyUserViewSet(viewsets.ModelViewSet):
    queryset = MyUser.objects.all()
    serializer_class = MyUserSerializer

    def get_permissions(self):
        if self.action == 'list':
            # список всех пользователей только для админа
            permission_classes = [permissions.IsAdminUser]
        elif self.action == 'create':
            # создание нового пользователя доступно всем (регистрация)
            permission_classes = [permissions.AllowAny]
        else:
            # просмотр/изменение — только сам или админ
            permission_classes = [IsAdminOrSelf]
        return [permission() for permission in permission_classes]


# Коды для 2FA
class Email2FACodeViewSet(viewsets.ModelViewSet):
    queryset = Email2FACode.objects.all()
    serializer_class = Email2FACodeSerializer

    def get_permissions(self):
        if self.action in ['list', 'create']:
            # Админ может видеть все коды и создавать
            permission_classes = [permissions.IsAdminUser]
        else:
            # Обычный юзер может работать только со своими кодами
            permission_classes = [IsAdminOrSelf]
        return [permission() for permission in permission_classes]


class LoginWith2FAView(APIView):
    """
    Шаг 1: логин по паролю -> создаём код и шлём на почту
    """
    def post(self, request):
        username = request.data.get("username")
        password = request.data.get("password")

        user = authenticate(username=username, password=password)
        if not user:
            return Response({"detail": "Неверный логин или пароль"}, status=status.HTTP_401_UNAUTHORIZED)

        # генерим код
        code = str(random.randint(100000, 999999))

        # сохраняем или обновляем
        obj, created = Email2FACode.objects.update_or_create(
            user=user, defaults={"code": code}
        )

        from django.core.mail import send_mail
        from django.conf import settings

        send_mail(
            "Ваш код подтверждения",
            f"Ваш код: {code}",
            settings.DEFAULT_FROM_EMAIL,  # отправитель
            [user.email],  # получатель
            fail_silently=False,
        )

        return Response({"detail": "Код отправлен на почту"})


class Verify2FAView(APIView):
    """
    Шаг 2: подтверждение кода -> выдаём JWT
    """
    def post(self, request):
        username = request.data.get("username")
        code = request.data.get("code")

        try:
            user = MyUser.objects.get(username=username)
            code_obj = Email2FACode.objects.get(user=user)
        except (MyUser.DoesNotExist, Email2FACode.DoesNotExist):
            return Response({"detail": "Пользователь или код не найдены"}, status=status.HTTP_400_BAD_REQUEST)

        if code_obj.code != code:
            return Response({"detail": "Неверный код"}, status=status.HTTP_400_BAD_REQUEST)

        if code_obj.is_expired():
            return Response({"detail": "Код просрочен"}, status=status.HTTP_400_BAD_REQUEST)

        # выдаём JWT токен
        refresh = RefreshToken.for_user(user)
        return Response({
            "refresh": str(refresh),
            "access": str(refresh.access_token)
        })
