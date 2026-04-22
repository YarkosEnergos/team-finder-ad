from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.safestring import mark_safe
from users.forms import NewUserChangeForm, RegisterForm
from users.models import Skill, User

admin.site.register(Skill)


@admin.register(User)
class NewUserAdmin(UserAdmin):
    form = NewUserChangeForm

    list_display = ('get_avatar', 'email', 'username', 'name',
                    'surname', 'phone', 'is_staff')

    fieldsets = UserAdmin.fieldsets + (
        ('Дополнительная информация', {
            'fields': ('name', 'surname', 'phone', 'avatar', 'github_url', 'about', 'skills'),
        }),
    )

    add_form = RegisterForm

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'name', 'surname', 'phone', 'password'),
        }),
    )

    @admin.display(description='Аватар')
    def get_avatar(self, obj):
        if obj.avatar:
            return mark_safe(f'<img src="{obj.avatar.url}" width="50" height="50" style="object-fit: cover; border-radius: 50%;">')
        return "Нет фото"
