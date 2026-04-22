import os
from io import BytesIO

from common.constants import (AVATAR_BG_COLOR, AVATAR_SIZE, BBOX_START,
                              FONT_SIZE, SKILL_NAME_LENGTH, TEXT_COLOR,
                              USER_ABOUT_LENGTH, USER_NAME_LENGTH,
                              USER_PHONE_LENGTH)
from django.contrib.auth.models import AbstractUser, UserManager
from django.core.files.base import ContentFile
from django.db import models
from PIL import Image, ImageDraw, ImageFont


class Skill(models.Model):
    name = models.CharField(max_length=SKILL_NAME_LENGTH, verbose_name='Навык')

    class Meta:
        verbose_name = 'Навык'
        verbose_name_plural = 'Навыки'

    def __str__(self):
        return self.name


class User(AbstractUser):
    email = models.EmailField(unique=True, verbose_name='Электронная почта')
    name = models.CharField(max_length=USER_NAME_LENGTH, verbose_name='Имя')
    surname = models.CharField(
        max_length=USER_NAME_LENGTH,
        verbose_name='Фамилия'
    )
    username = models.CharField(
        max_length=USER_NAME_LENGTH,
        blank=True,
        verbose_name="Ник"
    )
    avatar = models.ImageField(
        upload_to='avatars/',
        blank=True,
        verbose_name='Аватар'
    )
    phone = models.CharField(
        max_length=USER_PHONE_LENGTH,
        blank=True,
        verbose_name='Телефон'
    )
    github_url = models.URLField(blank=True, verbose_name='GitHub')
    about = models.TextField(
        max_length=USER_ABOUT_LENGTH,
        blank=True,
        verbose_name='О себе'
    )
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

    def save(self, *args, **kwargs):
        if not self.avatar:
            self.generate_avatar()

        super().save(*args, **kwargs)

    def generate_avatar(self):

        letter = self.name[0].upper()

        size = AVATAR_SIZE
        img = Image.new("RGB", (size, size), AVATAR_BG_COLOR)
        draw = ImageDraw.Draw(img)

        current_dir = os.path.dirname(os.path.abspath(__file__))
        font_path = os.path.join(
            current_dir, "Neue_Haas_Grotesk_Display_Pro_75_Bold.otf")

        try:
            font = ImageFont.truetype(font_path, FONT_SIZE)
        except Exception:
            font = ImageFont.load_default()

        bbox = draw.textbbox(BBOX_START, letter, font=font)
        text_width = bbox[2] - bbox[0]
        text_height = bbox[3] - bbox[1]

        position = (
            (size - text_width) / 2 - bbox[0],
            (size - text_height) / 2 - bbox[1]
        )

        draw.text(position, letter, fill=TEXT_COLOR, font=font)

        buffer = BytesIO()
        img.save(buffer, format="PNG")

        file_name = f"{self.email}_avatar.png"
        self.avatar.save(file_name, ContentFile(buffer.getvalue()), save=False)
