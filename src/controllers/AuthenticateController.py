import logging
import os
from typing import Dict

from .Controller import Controller
from views.LoginView import LoginView

log = logging.getLogger(__name__)
log.setLevel(getattr(logging, os.environ.get("LOG_LEVEL", "info").upper()))


class AuthenticateController(Controller):
    _passcode_validator: "PasscodeValidator"
    _jwt_generator: "JwtGenerator"
    _jwt_validator: "JwtValidator"
    _csrf_token_validator: "CsrfTokenValidator"
    _survey_uri: str
    
    def __init__(
            self,
            passcode_validator: "PasscodeValidator",
            jwt_generator: "JwtGenerator",
            jwt_validator: "JwtValidator",
            csrf_token_validator: "CsrfTokenValidator",
            survey_uri: str
    ):
        self._passcode_validator = passcode_validator
        self._jwt_generator = jwt_generator
        self._jwt_validator = jwt_validator
        self._csrf_token_validator = csrf_token_validator
        self._survey_uri = survey_uri
        
    def post(
            self,
            form: dict,
            headers: dict,
            multi_value_headers: dict
    ) -> dict:
        try:
            cookie_map: Dict[str, str] = {}
            for cookie in multi_value_headers["Cookie"]:
                name, value = cookie.split("=")
                cookie_map[name] = value
        except KeyError:
            log.warn("No cookies. Redirecting to login")
            return self.__class__.redirect("/?failureReason=timeout")
        
        jwt: str = cookie_map["session"]
        if not self._jwt_validator.is_valid_jwt(jwt):
            log.warn("Invalid JWT. Redirecting to login")
            return self.__class__.redirect("/?failureReason=timeout")

        csrf_token: str = form["csrf-token"][0]
        log.info("CSRF token exists in form. Checking...")
        log.debug(f"CSRF token: {csrf_token}")
        if not self._csrf_token_validator.is_valid_csrf_token(
                csrf_token,
                self._jwt_validator.get_sub(jwt)                
        ):
            log.warn("Invalid CSRF token. Redirecting to login")
            return self.__class__.redirect("/?failureReason=timeout")

        passcode: str = form["passcode"][0]
        log.info("Passcode exists in form. Checking...")
        log.debug(f"Passcode is {passcode}")
        session_secret: str = self.build_session_secret(headers["User-Agent"])
        if self._passcode_validator.is_valid_passcode(passcode):
            log.info("Valid passcode. Redirecting to survey")
            sso_token: str = self._jwt_generator.build_jwt(session_secret)
            return self.__class__.redirect(
                f"{self._survey_uri}?token={sso_token}"
            )

        log.warn("Invalid passcode. Responding with login screen with error message")
        return self.__class__.redirect("/?failureReason=passcode")
