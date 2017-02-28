from __future__ import unicode_literals

from django.db import models
from django.contrib import admin
from django.utils import timezone
from django.contrib.auth.models import(
    BaseUserManager, AbstractBaseUser, PermissionsMixin)
from django.db.models.signals import m2m_changed
from django.contrib.postgres.fields import ArrayField, JSONField

# Create your models here.
class TimeStampModel(models.Model):
    added_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class CustomUserManager(BaseUserManager):

    def _create_user(self, email, password, is_staff, is_superuser, **extra_fields):
        is_active = extra_fields.pop("is_active", False)
        now = timezone.now()
        if not email:
            raise ValueError('Email must be provided')
        email = self.normalize_email(email)
        user = self.model(email=email,
                          is_staff=is_staff, is_active=is_active,
                          is_superuser=is_superuser, last_login=now,
                          date_joined=now, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        extra_fields.update({'is_active': True})
        return self._create_user(email, password, False, False, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.update({'is_active': True})
        return self._create_user(email, password, True, True, **extra_fields)


class BaseUser(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(max_length=255, blank=True)
    email = models.EmailField(max_length=255, unique=True)
    first_name = models.CharField(max_length=100, default='')
    last_name = models.CharField(max_length=100, default='')
    name = models.CharField(max_length=100, default='')
    full_name = models.CharField(max_length=100)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    date_joined = models.DateTimeField(default=timezone.now)
    objects = CustomUserManager()

    USERNAME_FIELD = 'email'

    def get_short_name(self):
        return self.full_name

    def __str__(self):
        return self.email
