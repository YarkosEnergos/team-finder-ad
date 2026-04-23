from common.constants import (PROJECT_NAME_LENGTH, PROJECT_STATUS_CHOICES,
                              PROJECT_STATUS_LENGTH, STATUS_OPEN)
from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class Project(models.Model):
    name = models.CharField(
        max_length=PROJECT_NAME_LENGTH, verbose_name='Название'
    )
    description = models.TextField(verbose_name='Описание')
    owner = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='owned_projects',
        verbose_name='Владелец',
    )
    created_at = models.DateField(
        auto_now_add=True,
        verbose_name='Дата создания'
    )
    github_url = models.URLField(
        blank=True,
        verbose_name='GitHub'
    )
    status = models.CharField(
        choices=PROJECT_STATUS_CHOICES,
        max_length=PROJECT_STATUS_LENGTH,
        default=STATUS_OPEN,
        verbose_name='Статус'
    )
    participants = models.ManyToManyField(
        User,
        blank=True,
        related_name="participated_projects",
        verbose_name='Участники'
    )

    class Meta:
        verbose_name = 'Проект'
        verbose_name_plural = 'Проекты'

    def __str__(self):
        return self.name
