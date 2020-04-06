import logging
import os
from typing import Dict, List

from .Controller import Controller
from views.SurveyView import SurveyView

log = logging.getLogger(__name__)
log.setLevel(getattr(logging, os.environ.get("LOG_LEVEL", "info").upper()))

class SurveyController(Controller):
    _view = SurveyView
    _LOGIN_URI: str = "/"
    _sso_jwt_validator: "..auth.JwtValidator"
    _session_jwt_validator: "..auth.JwtValidator"
    _jwt_generator: "..auth.JwtGenerator"
    FIFTEEN_MINUTES_IN_SECONDS: int = 15 * 60

    def __init__(
        self,
        sso_jwt_validator: "..auth.JwtValidator",
        session_jwt_validator: "..auth.JwtValidator",
        jwt_generator: "..auth.JwtGenerator"
    ):
        self._sso_jwt_validator = sso_jwt_validator
        self._session_jwt_validator = session_jwt_validator
        self._jwt_generator = jwt_generator

    def get(self, query_string: dict) -> dict:
        token: str = query_string.get("token")
        log.debug(f"SSO Token: {token} of type {type(token)}")
        if token and self._sso_jwt_validator.is_valid_jwt(token):
            log.info("SSO succeeded. Generating session token")
            log.info("Responding with session JWT and survey HTML")
            return self.__class__.respond_with_html(
                SurveyView.get_html(),
                set_cookie_header=self._build_cookie_header()
            )
        else:
            log.warn("Invalid SSO token. Redirecting to login")
            return self.__class__.redirect(self._LOGIN_URI)

    def post(
            self,
            form: Dict[str, List[str]],
            headers: Dict
    ) -> dict:
        cookies: List[str] = headers.get("Cookie")
        log.debug(f"Headers: {headers}")
        log.info(f"Cookies: {cookies}")
        if cookies and self._session_jwt_validator.is_valid_jwt(cookies[0]):
            log.info("Valid JWT")
            return self.__class__.redirect("http://google.com")

        log.warn("Invalid JWT")
        return self.__class__.redirect(self._LOGIN_URI)
        
    def _build_cookie_header(self) -> str:
        return "session={0};Domain={1};Path={2};Max-Age={3};SameSite=Lax;HttpOnly;Secure;".format(
            "this-is-bogus",#self._jwt_generator.build_jwt(),
            "rsvp.adriandmikejones.com",
            "/survey",
            self.FIFTEEN_MINUTES_IN_SECONDS,
        )
