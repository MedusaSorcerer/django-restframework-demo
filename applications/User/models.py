# _*_ Coding: UTF-8 _*_
from uuid import uuid4

from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import ugettext_lazy as _


class User(AbstractUser):
    user_secret = models.UUIDField(default=uuid4(), help_text=_('user secret'))

    class Meta:
        db_table = 'medusa_user'
        ordering = ('-id',)
