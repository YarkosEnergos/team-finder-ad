from django.db import models
from django.contrib.auth import get_user_model

STATUS_CHOICES = [
    ("open", "Open"),
    ("closed", "Closed"),
]

User = get_user_model()


class Project(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    owner = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='owned_projects',
    )
    created_at = models.DateField(auto_now_add=True)
    github_url = models.URLField(blank=True)
    status = models.CharField(choices=STATUS_CHOICES, max_length=6)
    participants = models.ManyToManyField(
        User, blank=True,
        related_name="participated_projects")

    def __str__(self):
        return self.name
