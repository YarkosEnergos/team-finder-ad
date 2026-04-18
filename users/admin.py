from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .forms import CustomUserCreationForm, CustomUserChangeForm
from .models import User, Skill

admin.site.register(Skill)


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    form = CustomUserChangeForm

    list_display = ('email', 'username', 'name',
                    'surname', 'phone', 'is_staff')

    fieldsets = UserAdmin.fieldsets + (
        ('Дополнительная информация', {
            'fields': ('name', 'surname', 'phone', 'avatar', 'github_url', 'about', 'skills'),
        }),
    )

    add_form = CustomUserCreationForm

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'username', 'name', 'surname', 'phone', 'password1', 'password2'),
        }),
    )
