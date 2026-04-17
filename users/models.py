from django.contrib.auth.models import AbstractUser, UserManager
from django.db import models


class Skill(models.Model):
    name = models.CharField(max_length=124)

    def __str__(self):
        return self.name


class User(AbstractUser):
    email = models.EmailField(unique=True)
    name = models.CharField(max_length=124)
    surname = models.CharField(max_length=124)
    avatar = models.ImageField(upload_to='avatars/', blank=True)
    phone = models.CharField(max_length=12)
    github_url = models.URLField(blank=True)
    about = models.TextField(max_length=256, blank=True)
    skills = models.ManyToManyField(
        Skill,
        related_name='users',
        blank=True,
    )
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    objects = UserManager()

    def __str__(self):
        return self.email
