
from django.db import models
from django.contrib.auth.models import AbstractUser

from django.contrib.auth.models import BaseUserManager


class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('Email is required')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        # اینجا نباید ورودی username داشته باشیم
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(email, password, **extra_fields)


# در مدل اصلی کاربر هم مطمئن شو این تنظیمات هست:
class User(AbstractUser):
    username = None  # حذف فیلد یوزرنیم
    email = models.EmailField(unique=True)

    USERNAME_FIELD = 'email'  # ایمیل به عنوان شناسنامه کاربر
    REQUIRED_FIELDS = []  # فیلد اضافی برای createsuperuser نمی‌خواهیم

    objects = UserManager()  # اتصال منیجر جدید