from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from user.views import MyUserViewSet, Email2FACodeViewSet, RegisterView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

# Роутер для ViewSet'ов
router = DefaultRouter()
router.register(r'users', MyUserViewSet, basename="user")
router.register(r'codes', Email2FACodeViewSet, basename="code")

urlpatterns = [

    # роуты из DRF (users, codes)
    path('api/', include(router.urls)),

    # регистрация
    path('register/', RegisterView.as_view(), name='register'),

    # JWT авторизация
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]

