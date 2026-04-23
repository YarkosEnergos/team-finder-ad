import re

from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import AuthenticationForm, UserChangeForm
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError

from common.validators import validate_github_url


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


class NewUserChangeForm(UserChangeForm):
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

        return validate_github_url(github_url)
