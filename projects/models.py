from django.db import models
from django.contrib.auth import get_user_model

STATUS_CHOICES = [
    ("open", "Открыт"),
    ("closed", "Закрыт"),
]

User = get_user_model()


class Project(models.Model):
    name = models.CharField(max_length=200, verbose_name='Название')
    description = models.TextField(verbose_name='Описание')
    owner = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='owned_projects',
        verbose_name='Владелец',
    )
    created_at = models.DateField(auto_now_add=True, verbose_name='Дата создания')
    github_url = models.URLField(blank=True, verbose_name='GitHub')
    status = models.CharField(choices=STATUS_CHOICES, max_length=6, verbose_name='Статус')
    participants = models.ManyToManyField(
        User, blank=True,
        related_name="participated_projects",
        verbose_name='Участники'
    )

    class Meta:
        verbose_name = 'Проект'
        verbose_name_plural = 'Проекты'

    def __str__(self):
        return self.name
