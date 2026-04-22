from django.contrib.auth.models import AbstractUser, UserManager
from django.db import models

from io import BytesIO
from PIL import Image, ImageDraw, ImageFont
from django.core.files.base import ContentFile

import os


AVATAR_BG_COLOR = "#6C5CE7"


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

    def generate_avatar(self):

        letter = self.name[0].upper()

        size = 200
        img = Image.new("RGB", (size, size), AVATAR_BG_COLOR)
        draw = ImageDraw.Draw(img)

        current_dir = os.path.dirname(os.path.abspath(__file__))
        font_path = os.path.join(
            current_dir, "Neue_Haas_Grotesk_Display_Pro_75_Bold.otf")

        try:
            font = ImageFont.truetype(font_path, 100)
        except Exception as e:
            print(f"Ошибка загрузки шрифта: {e}")
            font = ImageFont.load_default()

        bbox = draw.textbbox((0, 0), letter, font=font)
        text_width = bbox[2] - bbox[0]
        text_height = bbox[3] - bbox[1]

        position = (
            (size - text_width) / 2 - bbox[0],
            (size - text_height) / 2 - bbox[1]
        )

        draw.text(position, letter, fill="white", font=font)

        buffer = BytesIO()
        img.save(buffer, format="PNG")

        file_name = f"{self.email}_avatar.png"
        self.avatar.save(file_name, ContentFile(buffer.getvalue()), save=False)

    def save(self, *args, **kwargs):
        if not self.avatar:
            self.generate_avatar()

        super().save(*args, **kwargs)

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return self.email
