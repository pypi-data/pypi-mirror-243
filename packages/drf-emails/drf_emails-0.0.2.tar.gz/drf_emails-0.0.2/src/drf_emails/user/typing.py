from typing import Any, Type

from drf_emails.user.abstracts import AbstractCodeVerify


Kwargs = dict[str, Any]
Code = Type[AbstractCodeVerify]
