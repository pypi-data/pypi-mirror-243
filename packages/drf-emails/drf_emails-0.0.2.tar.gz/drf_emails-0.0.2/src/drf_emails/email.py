from typing import Callable, Optional, Any

from drf_emails.typing import TemplateFiles, Context
from drf_emails.utils import send_multi_format_email, get_template_files


class Email:
    def __init__(self, prefix: str, folder: str = "") -> None:
        self._prefix = prefix
        self._folder = folder
        self._templates: Optional[TemplateFiles] = None

    def __str__(self) -> str:
        return '%s [%s, %s]' % (
            self.__class__.__name__,
            self._folder,
            self._prefix,
        )

    @property
    def templates(self):
        if self._templates is not None:
            return self._templates

        self._templates = get_template_files(
            folder=self._folder,
            prefix=self._prefix,
        )
        return self._templates

    def get_send_email_callable(self) -> Callable[..., Any]:
        """Return the send email callable."""
        return send_multi_format_email

    def send_email(self, target: str, context: Context) -> None:
        self.get_send_email_callable()(
            context=context,
            target_email=target,

            templates=self.templates,
        )
