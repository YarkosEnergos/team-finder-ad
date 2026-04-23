from django.contrib import admin

from .models import Project


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ['name', 'description', 'owner__name', 'created_at',
                    'github_url', 'status', 'participants__name']
    search_fields = ['name', 'owner__name']
    list_filter = ['status']
