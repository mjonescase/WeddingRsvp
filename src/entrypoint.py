from datetime import timedelta
import json
import logging
import os
from typing import Dict, List
from urllib.parse import parse_qs

from auth.CsrfTokenGenerator import CsrfTokenGenerator
from auth.CsrfTokenValidator import CsrfTokenValidator
from auth.PasscodeValidator import hash_passcode, PasscodeValidator
from auth.JwtGenerator import JwtGenerator
from auth.JwtValidator import JwtValidator
from controllers.AuthenticateController import AuthenticateController
from controllers.LoginController import LoginController
from controllers.SurveyController import SurveyController
from secret_dao import get_secret

log = logging.getLogger(__name__)
log.setLevel(getattr(logging, os.environ.get("LOG_LEVEL", "info").upper()))

# read environment variables, set constants
HASHED_PASSCODE: str = hash_passcode("LOTS_OF_PASSCODE".lower())
ANONYMOUS_JWT_SECRET: bytes = hash_passcode("LOTS_OF_SECRET").encode("utf-8")
SSO_JWT_SECRET: bytes = hash_passcode("LOTS_OF_SSO").encode("utf-8")
SESSION_SECRET: bytes = hash_passcode("LOTS_OF_SESSION").encode("utf-8")
CSRF_SECRET: bytes = hash_passcode("LOTS_OF_CSRF").encode("utf-8")
AWS_SAM_LOCAL: str = os.environ.get("AWS_SAM_LOCAL")
log.info(f"AWS_SAM_LOCAL: {AWS_SAM_LOCAL}")
if not AWS_SAM_LOCAL or AWS_SAM_LOCAL.lower() == "false":
    log.info("Not local. Getting real secrets from secretsmanager")
    HASHED_PASSCODE = get_secret(os.environ["PASSCODE_ARN"])["RsvpPassword"]
    ANONYMOUS_JWT_SECRET = get_secret(os.environ["ANONYMOUS_JWT_SECRET_ARN"])["RsvpJwtSecret"].encode("utf-8")
    SSO_JWT_SECRET = get_secret(os.environ["SSO_JWT_SECRET_ARN"])["RsvpJwtSecret"].encode("utf-8")
    SESSION_SECRET = get_secret(os.environ["SESSION_TOKEN_SECRET_ARN"])["RsvpJwtSecret"].encode("utf-8")
    CSRF_SECRET = get_secret(os.environ["CSRF_TOKEN_SECRET_ARN"])["CsrfTokenSecret"].encode("utf-8")
else:
    log.info("Running locally for development or testing")

CONTROLLER: str = os.environ["CONTROLLER"]
log.info(f"controller setting: {CONTROLLER}")

# initialize controllers
login_controller: LoginController = LoginController(
    JwtGenerator(ANONYMOUS_JWT_SECRET, 1, "minutes"),
    CsrfTokenGenerator(CSRF_SECRET, "login"),
)

authenticate_controller: AuthenticateController = AuthenticateController(
    PasscodeValidator(HASHED_PASSCODE),
    JwtGenerator(SSO_JWT_SECRET, 10, "seconds"),
    JwtValidator(ANONYMOUS_JWT_SECRET),
    CsrfTokenValidator(CSRF_SECRET, "login", timedelta(minutes=1)),
    os.environ["SURVEY_URI"]    
)

survey_controller: SurveyController = SurveyController(
    JwtValidator(SSO_JWT_SECRET),
    JwtGenerator(SESSION_SECRET, 15, "minutes"),
    CsrfTokenGenerator(CSRF_SECRET, "survey")    
)

#choose controller based on CONTROLLER environment variable
controller: "Controller" = globals()[f"{CONTROLLER}_controller"]

def lambda_handler(event, _):
    log.info("WeddingRsvp common lambda entrypoint reached")
    log.debug(f"Event: {event}")
    return {
        "get": _handle_get,
        "post": _handle_post,
    }[event["httpMethod"].lower()](event)


def _handle_get(event):
    query_string: Dict[str, str] = event["queryStringParameters"]
    log.info("Handling GET request")
    log.info(f"Query string: {query_string}")
    headers: dict = event["headers"]
    log.debug(f"Single value headers: {headers}")
    multi_value_headers: dict = event["multiValueHeaders"]
    log.debug(f"Multi value headers: {multi_value_headers}")
    return controller.get(query_string or {}, headers, multi_value_headers)


def _handle_post(event):
    log.info("Handling POST request")
    multi_value_headers: dict = event["multiValueHeaders"]
    headers: dict = event["headers"]
    log.debug(f"MultiValueHeaders: {multi_value_headers}")
    log.debug(f"Headers: {headers}")
    user_agent: str = headers["User-Agent"]
    log.debug(f"User-Agent: {user_agent}")
    return controller.post(parse_qs(event['body']), headers, multi_value_headers)
