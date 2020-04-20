from datetime import timedelta
import logging
import os
from typing import Dict, List

from .Controller import Controller
from views.MultiPageSurveyView import MultiPageSurveyView as SurveyView

log = logging.getLogger(__name__)
log.setLevel(getattr(logging, os.environ.get("LOG_LEVEL", "info").upper()))

class SurveyController(Controller):
    _view = SurveyView
    _LOGIN_URI: str = "/"
    _COOKIE_DURATION = timedelta(minutes=15)
    _sso_jwt_validator: "..auth.JwtValidator"
    _session_jwt_generator: "..auth.JwtGenerator"
    _csrf_token_generator: "..auth.CsrfTokenGenerator"

    def __init__(
            self,
            sso_jwt_validator: "..auth.JwtValidator",
            session_jwt_generator: "..auth.JwtGenerator",
            csrf_token_generator: "..auth.CsrfTokenGenerator",
    ):
        self._sso_jwt_validator = sso_jwt_validator
        self._session_jwt_generator = session_jwt_generator
        self._csrf_token_generator = csrf_token_generator

    def get(
            self,
            query_string: dict,
            headers: dict,
            multi_value_headers: dict
    ) -> dict:
        token: str = query_string.get("token")
        log.debug(f"SSO Token: {token} of type {type(token)}")
        if token and self._sso_jwt_validator.is_valid_jwt(token):
            log.info("SSO succeeded. Generating session token")
            log.info("Responding with session JWT and survey HTML")
            session_secret: str = self.build_session_secret(headers["User-Agent"])
            csrf_token: str = self._csrf_token_generator.build_csrf_token(session_secret)
            return {
                "statusCode": 200,
                "body": SurveyView.get_html(csrf_token),
                "headers": {
                    "Set-Cookie": self.build_session_cookie(
                        self._session_jwt_generator.build_jwt(subject=session_secret),
                        self._COOKIE_DURATION
                    ),
                    "Content-Type": "text/html"
                }
            }

        else:
            log.warn("Invalid SSO token. Redirecting to login")
            return self.__class__.redirect(self._LOGIN_URI)
