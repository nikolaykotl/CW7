from django.contrib.auth.models import AbstractUser

from django.db import models

NULLABLE = {'blank': True, 'null': True}


class User(AbstractUser):
    username = None
    email = models.EmailField(unique=True, verbose_name='email')

    phone = models.CharField(max_length=20, verbose_name='телефон', **NULLABLE)
    avatar = models.ImageField(upload_to='users/', verbose_name='аватар',
                               **NULLABLE)
    city = models.CharField(max_length=100, verbose_name='город', **NULLABLE)
    tg_id = models.IntegerField(verbose_name="id пользователя телеграмм",
                                **NULLABLE)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
