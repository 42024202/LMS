from rest_framework import viewsets, permissions
from .models import MyUser, Email2FACode
from .serializers import MyUserSerializer, Email2FACodeSerializer
from .permissions import IsAdminOrSelf


class MyUserViewSet(viewsets.ModelViewSet):
    queryset = MyUser.objects.all()
    serializer_class = MyUserSerializer

    def get_permissions(self):
        if self.action in ['list', 'create']:
            # Список всех пользователей и создание новых — только для админа
            permission_classes = [permissions.IsAdminUser]
        else:
            # Остальное — по нашему правилу (свои данные или админ)
            permission_classes = [IsAdminOrSelf]
        return [permission() for permission in permission_classes]


class Email2FACodeViewSet(viewsets.ModelViewSet):
    queryset = Email2FACode.objects.all()
    serializer_class = Email2FACodeSerializer

    def get_permissions(self):
        if self.action in ['list', 'create']:
            # Админ может видеть все коды и создавать
            permission_classes = [permissions.IsAdminUser]
        else:
            # Обычный может только свои коды
            permission_classes = [IsAdminOrSelf]
        return [permission() for permission in permission_classes]
