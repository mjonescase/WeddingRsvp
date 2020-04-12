from datetime import datetime, timedelta, timezone

import csrf

class CsrfTokenValidator:
    _csrf_secret: bytes
    _form_id: str
    _duration: timedelta

    def __init__(
            self,
            csrf_secret: bytes,
            form_id: str,
            duration: timedelta
    ):
        self._csrf_secret = csrf_secret
        self._form_id = form_id
        self._duration = duration

    def is_valid_csrf_token(self, token: str, session_secret: str) -> bool:
        return csrf.valid(
            self._csrf_secret,
            session_secret.encode("utf-8"),
            self._form_id,
            (timedelta(), self._duration),
            datetime.now(timezone.utc),
            token
        )
