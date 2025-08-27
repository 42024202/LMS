from django.urls import path, include
from rest_framework.routers import DefaultRouter
from user.views import MyUserViewSet, Email2FACodeViewSet, RegisterView, LoginWith2FAView, Verify2FAView
from rest_framework_simplejwt.views import TokenRefreshView

router = DefaultRouter()
router.register(r'users', MyUserViewSet, basename="user")
router.register(r'codes', Email2FACodeViewSet, basename="code")

urlpatterns = [
    path('api/', include(router.urls)),

    # регистрация
    path('register/', RegisterView.as_view(), name='register'),

    # 2FA логин
    path('login/', LoginWith2FAView.as_view(), name='login_with_2fa'),
    path('verify-2fa/', Verify2FAView.as_view(), name='verify_2fa'),

    # обновление токена
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]

