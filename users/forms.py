import re
from urllib.parse import urlparse

from django.contrib.auth.forms import UserChangeForm, AuthenticationForm
from django import forms
from django.core.exceptions import ValidationError
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth import get_user_model


User = get_user_model()


class RegisterForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('name', 'surname', 'email', 'password')

    def clean_password(self):
        password = self.cleaned_data.get('password')

        try:
            validate_password(password, self.instance)
        except ValidationError as e:
            raise ValidationError(e.messages)

        return password


class EmailAuthenticationForm(AuthenticationForm):
    username = forms.EmailField(
        label='Email',
        widget=forms.EmailInput(attrs={'autofocus': True})
    )

    class Meta:
        model = User
        fields = ('username', 'password')


class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = User
        fields = ('name', 'surname', 'phone',
                  'avatar', 'github_url', 'about')

    def clean_phone(self):
        phone = self.cleaned_data.get('phone')

        if not phone:
            return phone

        if re.fullmatch(r'8\d{10}', phone):
            normalized_phone = '+7' + phone[1:]
        elif re.fullmatch(r'\+7\d{10}', phone):
            normalized_phone = phone
        else:
            raise ValidationError(
                "Номер должен быть в формате 8XXXXXXXXXX или +7XXXXXXXXXX"
            )

        qs = User.objects.filter(phone=normalized_phone)

        if self.instance.pk:
            qs = qs.exclude(pk=self.instance.pk)

        if qs.exists():
            raise ValidationError("Этот номер уже используется")

        return normalized_phone

    def clean_github_url(self):
        github_url = self.cleaned_data.get('github_url')

        if not github_url:
            return github_url

        parsed = urlparse(github_url)

        if parsed.scheme not in ('http', 'https'):
            raise ValidationError(
                "Ссылка должна начинаться с http:// или https://")

        if parsed.netloc not in ('github.com', 'www.github.com'):
            raise ValidationError("Ссылка должна вести на github.com")

        return github_url
