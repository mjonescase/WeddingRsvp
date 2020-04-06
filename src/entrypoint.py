import json
import logging
import os
from typing import Dict, List
from urllib.parse import parse_qs

from auth.PasscodeValidator import hash_passcode, PasscodeValidator
from auth.JwtGenerator import JwtGenerator
from auth.JwtValidator import JwtValidator
from controllers.LoginController import LoginController
from controllers.SurveyController import SurveyController
from secret_dao import get_secret

log = logging.getLogger(__name__)
log.setLevel(getattr(logging, os.environ.get("LOG_LEVEL", "info").upper()))

# read environment variables, set constants
HASHED_PASSCODE: str = hash_passcode("LOTS_OF_PASSCODE".lower())
JWT_SECRET: bytes = hash_passcode("LOTS_OF_SECRET").encode("utf-8")
SESSION_SECRET: bytes = hash_passcode("LOTS_OF_SESSION").encode("utf-8")
AWS_SAM_LOCAL: str = os.environ.get("AWS_SAM_LOCAL")
log.info(f"AWS_SAM_LOCAL: {AWS_SAM_LOCAL}")
if not AWS_SAM_LOCAL or AWS_SAM_LOCAL.lower() == "false":
    log.info("Not local. Getting real secrets from secretsmanager")
    HASHED_PASSCODE = get_secret(os.environ["PASSCODE_ARN"])["RsvpPassword"]
    JWT_SECRET = get_secret(os.environ["JWT_SECRET_ARN"])["RsvpJwtSecret"].encode("utf-8")
    SESSION_SECRET = get_secret(os.environ["SESSION_TOKEN_SECRET_ARN"])["RsvpJwtSecret"].encode("utf-8")
else:
    log.info("Running locally for development or testing")

CONTROLLER: str = os.environ["CONTROLLER"]
log.info(f"controller setting: {CONTROLLER}")

# initialize controllers
login_controller: LoginController = LoginController(
    PasscodeValidator(HASHED_PASSCODE),
    JwtGenerator(JWT_SECRET, 10, "seconds"),
    os.environ["SURVEY_URI"]
)

survey_controller: SurveyController = SurveyController(
    JwtValidator(JWT_SECRET),
    JwtValidator(SESSION_SECRET),
    JwtGenerator(SESSION_SECRET, 15, "minutes")
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
    return controller.get(query_string or {})


def _handle_post(event):
    log.info("Handling POST request")
    multi_value_headers: dict = event["multiValueHeaders"]
    log.debug(f"MultiValueHeaders: {multi_value_headers}")
    return controller.post(parse_qs(event['body']), multi_value_headers)
