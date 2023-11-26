from typing import Optional
from django.urls import reverse_lazy

from drf_emails.typing import Context
from drf_emails.email import Email
from drf_emails.settings import settings


class CodeVerifyEmail(Email):
    def __init__(
        self,
        *args,
        link_to_url: Optional[str] = None,
        **kwargs,
    ) -> None:
        # `link_to_url` is needed in case there is no client link and the
        # email should return the URL for specific view
        self.link_to_url = link_to_url

        super().__init__(*args, **kwargs)

    @property
    def _default_link(self):
        if hasattr(self, '_link'):
            return self._link

        self._link = (
            settings.USER_EMAILS_DEFAULT_ORIGIN
            + reverse_lazy(self.link_to_url)
        )

        return self._link

    def handle_context_link(self, context: Context) -> Context:
        # Return unchanged context if the `link_to_url` attribute is missing
        if not self.link_to_url:
            return context

        if context.get('link') is None:
            raise AttributeError(
                f'For {self} class the `link` context attribute is required.',
            )

        # replace context link with default link when it is empty
        context['link'] = context.get('link') or self._default_link
        return context

    def send_email(self, target: str, context: Context) -> None:
        context['code'] = 'CheckCode'
        return super().send_email(target, self.handle_context_link(context))
