from urllib.parse import urlparse

from common.constants import GIT_URL
from django.core.exceptions import ValidationError


def validate_github_url(github_url):
    if not github_url:
        return github_url

    parsed = urlparse(github_url)

    if parsed.scheme not in ('http', 'https'):
        raise ValidationError(
            "Ссылка должна начинаться с http:// или https://")

    if parsed.netloc not in (GIT_URL, 'www.' + GIT_URL):
        raise ValidationError("Ссылка должна вести на github.com")

    return github_url
