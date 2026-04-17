from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Skill

admin.site.register(Skill)


@admin.register(User)
class CustomUserAdmin(UserAdmin):

    list_display = ('email', 'username', 'name', 'surname', 'is_staff')

    fieldsets = UserAdmin.fieldsets + (
        ('Дополнительно', {
            'fields': ('skills',),
        }),
    )

#     # 4. Настройка того, как редактировать пользователя в админке
#     # Мы берем стандартные наборы полей и добавляем твои кастомные (phone, skills и т.д.)
#     fieldsets = UserAdmin.fieldsets + (
#         ('Дополнительная информация', {'fields': (
#             'name', 'surname', 'phone', 'avatar', 'github_url', 'about', 'skills')}),
#     )

    # add_fieldsets = UserAdmin.add_fieldsets + (
    #     ('Дополнительная информация', {
    #      'fields': ('name', 'surname', 'phone')}),
    # )
