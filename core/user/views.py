from rest_framework import viewsets, permissions, generics
from .models import MyUser, Email2FACode
from .serializers import (
    MyUserSerializer,
    Email2FACodeSerializer,
    RegisterSerializer,
)
from .permissions import IsAdminOrSelf


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
