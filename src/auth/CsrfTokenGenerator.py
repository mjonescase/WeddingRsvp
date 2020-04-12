from datetime import datetime, timedelta, timezone
import hashlib

import csrf

class CsrfTokenGenerator:
    _csrf_secret: bytes
    _form_id: str

    def __init__(
            self,
            csrf_secret: bytes,
            form_id: str
    ):
        self._csrf_secret = csrf_secret
        self._form_id = form_id

    def build_csrf_token(self, session_secret: str):
        utc_now: "datetime" = datetime.now(timezone.utc)
        return csrf.generate(
            self._csrf_secret,
            session_secret.encode("utf-8"),
            self._form_id,
            utc_now
        )
