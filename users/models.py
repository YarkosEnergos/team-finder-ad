from django.contrib.auth.models import AbstractUser, UserManager
from django.db import models


class Skill(models.Model):
    name = models.CharField(max_length=124, verbose_name='Навык')

    class Meta:
        verbose_name = 'Навык'
        verbose_name_plural = 'Навыки'

    def __str__(self):
        return self.name


class User(AbstractUser):
    email = models.EmailField(unique=True, verbose_name='Электронная почта')
    name = models.CharField(max_length=124, verbose_name='Имя')
    surname = models.CharField(max_length=124, verbose_name='Фамилия')
    username = models.CharField(max_length=124, blank=True, verbose_name="Ник")
    avatar = models.ImageField(
        upload_to='avatars/', blank=True, verbose_name='Аватар')
    phone = models.CharField(max_length=12, blank=True, verbose_name='Телефон')
    github_url = models.URLField(blank=True, verbose_name='GitHub')
    about = models.TextField(max_length=256, blank=True, verbose_name='О себе')
    skills = models.ManyToManyField(
        Skill,
        related_name='users',
        blank=True,
        verbose_name='Навыки',
    )
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name', 'surname']

    objects = UserManager()

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return self.email
