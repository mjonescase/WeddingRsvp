import logging
import os

from .Controller import Controller
from views.LoginView import LoginView

log = logging.getLogger(__name__)
log.setLevel(getattr(logging, os.environ.get("LOG_LEVEL", "info").upper()))

class LoginController(Controller):
    _view = LoginView
    _passcode_validator: "..auth.PasscodeValidator"
    _jwt_generator: "..auth.JwtGenerator"
    _survey_uri: str
    
    def __init__(
            self,
            passcode_validator: "..auth.PasscodeValidator",
            jwt_generator: "..auth.JwtGenerator",
            survey_uri: str
    ):
        self._passcode_validator = passcode_validator
        self._jwt_generator = jwt_generator
        self._survey_uri = survey_uri

    def get(self, query_string: dict) -> dict:
        return self.__class__.respond_with_html(LoginView.get_html())

    def post(self, form: dict) -> dict:
        passcode: str = form["passcode"][0]
        log.info("Passcode exists in form. Checking...")
        log.debug(f"Passcode is {passcode}")
        if self._passcode_validator.is_valid_passcode(passcode):
            log.info("Valid passcode. Redirecting to survey")
            sso_token: str = self._jwt_generator.build_jwt()
            return self.__class__.redirect(
                f"{self._survey_uri}?token={sso_token}"
            )

        log.warn("Invalid passcode. Responding with login screen with error message")
        return self.__class__.respond_with_html(LoginView.get_html(False))
