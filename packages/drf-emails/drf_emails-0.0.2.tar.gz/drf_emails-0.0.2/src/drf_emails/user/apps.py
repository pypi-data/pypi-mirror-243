from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class DrfEmailsUserConfig(AppConfig):
    name = 'drf_emails.user'
    verbose_name = _('django-rest-framework-emails user')
