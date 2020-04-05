import logging
import os

from .Controller import Controller
from views.SurveyView import SurveyView

log = logging.getLogger(__name__)
log.setLevel(getattr(logging, os.environ.get("LOG_LEVEL", "info").upper()))

class SurveyController(Controller):
    _view = SurveyView
    _LOGIN_URI: str = "/"
    _jwt_validator: "..auth.JwtValidator"
    _jwt_generator: "..auth.JwtGenerator"

    def __init__(
        self,
        jwt_validator: "..auth.JwtValidator",
        jwt_generator: "..auth.JwtGenerator"
    ):
        self._jwt_validator = jwt_validator
        self._jwt_generator = jwt_generator

    def get(self, query_string: dict) -> dict:
        token: str = query_string["token"]
        if self._jwt_validator.is_valid_jwt(token):
            log.info("SSO succeeded. Generating session token")
            # generate a session token jwt
            # add session token jwt in Authorization header
            log.info("Responding with survey HTML")
            return self.__class__.respond_with_html(SurveyView.get_html())
        else:
            log.warn("Invalid SSO token. Redirecting to login")
            return self.__class__.redirect(self._LOGIN_URI)
