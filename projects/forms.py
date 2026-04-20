from django.forms import ModelForm
from .models import Project
from django.core.exceptions import ValidationError

from urllib.parse import urlparse


class ProjectModelForm(ModelForm):
    class Meta:
        model = Project
        fields = ('name', 'description', 'github_url', 'status')

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
