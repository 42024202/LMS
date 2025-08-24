from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.db import models
from django.utils import timezone
from datetime import timedelta
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import PermissionsMixin


class MyUserRoleEnum(models.TextChoices):
    STANDARD_USER = "student", _("Учащийся")
    ADMIN = "admin", _("Админ")
    TEACHER = "instructor", _("Преподователь")

class MyUserManager(BaseUserManager):
    def create_user(self, username, email, password=None):
        if not email:
            raise ValueError("У пользователя должен быть email")
        if not username:
            raise ValueError("У пользователя должно быть имя")

        email = self.normalize_email(email)
        user = self.model(username=username, email=email)
        user.set_password(password)
        user.is_active = True
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email, password=None):
        user = self.create_user(username=username, email=email, password=password)
        user.is_admin = True
        user.is_staff = True
        user.is_active = True
        user.role = MyUserRoleEnum.ADMIN
        user.is_superuser = True
        user.save(using=self._db)
        return user


class MyUser(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(max_length=50, unique=True)
    email = models.EmailField(max_length=50, unique=True)
    avatar = models.ImageField(upload_to="avatar", null=True, blank=True)
    role = models.CharField(max_length=50, choices=MyUserRoleEnum.choices, default=MyUserRoleEnum.STANDARD_USER)

    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    objects = MyUserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    def __str__(self):
        return self.username

    def has_perm(self, perm, obj=None):
        return self.is_admin or self.is_superuser
    def has_module_perms(self, app_label):
        return self.is_admin or self.is_superuser


class Email2FACode(models.Model):
    user = models.OneToOneField(MyUser, on_delete=models.CASCADE)
    code = models.CharField(max_length=6, verbose_name='6-значный код')
    created_at = models.DateTimeField(auto_now_add=True)

    def is_expired(self):
        return timezone.now() > self.created_at + timedelta(minutes=5)

    def __str__(self):
        return f"{self.user.email} — {self.code}"
