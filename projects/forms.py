from common.validators import validate_github_url
from django.forms import ModelForm
from projects.models import Project


class ProjectModelForm(ModelForm):
    class Meta:
        model = Project
        fields = ('name', 'description', 'github_url', 'status')

    def clean_github_url(self):
        github_url = self.cleaned_data.get('github_url')

        return validate_github_url(github_url)
