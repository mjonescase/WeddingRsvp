from datetime import timedelta
import logging
import os
from typing import Dict, List

from .Controller import Controller
from views.LoginView import LoginView

log = logging.getLogger(__name__)
log.setLevel(getattr(logging, os.environ.get("LOG_LEVEL", "info").upper()))


class LoginController(Controller):
    _COOKIE_DURATION = timedelta(minutes=1)
    _jwt_generator: "..auth.JwtGenerator"
    _csrf_token_generator: "..auth.CsrfTokenGenerator"
    
    def __init__(
            self,
            jwt_generator: "..auth.JwtGenerator",
            csrf_token_generator: "..auth.CsrfTokenGenerator",
    ):
        self._jwt_generator = jwt_generator
        self._csrf_token_generator = csrf_token_generator

    def get(
            self,
            _,
            headers: Dict[str, str],
            multi_value_headers: Dict[str, List[str]]
    ) -> dict:
        session_secret: str = self.build_session_secret(headers["User-Agent"])
        csrf_token: str = self._csrf_token_generator.build_csrf_token(session_secret)
        return {
            "statusCode": 200,
            "body": LoginView.get_html(csrf_token),
            "headers": {
                "Set-Cookie": self.build_session_cookie(
                    self._jwt_generator.build_jwt(subject=session_secret),
                    self._COOKIE_DURATION
                ),
                "Content-Type": "text/html"
            }
        }
