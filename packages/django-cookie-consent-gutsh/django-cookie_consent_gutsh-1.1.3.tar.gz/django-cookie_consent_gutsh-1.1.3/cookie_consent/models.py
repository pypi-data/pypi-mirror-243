from django.conf import settings

from django.db import models

class CookieConsentAcceptance(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, models.CASCADE,
        related_name='cookie_consent',
    )

    def __str__(self) -> str:
        return f'cookie consent obj for user "{self.user.username}"'
