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
JWT_SECRET: str = hash_passcode("LOTS_OF_SECRET")
SESSION_SECRET: str = hash_passcode("LOTS_OF_SESSION")
AWS_SAM_LOCAL: str = os.environ.get("AWS_SAM_LOCAL")
log.info(f"AWS_SAM_LOCAL: {AWS_SAM_LOCAL}")
if not AWS_SAM_LOCAL or AWS_SAM_LOCAL.lower() == "false":
    log.info("Not local. Getting real secrets from secretsmanager")
    HASHED_PASSCODE = get_secret(os.environ["PASSCODE_ARN"])["RsvpPassword"]
    JWT_SECRET = get_secret(os.environ["JWT_SECRET_ARN"])["RsvpJwtSecret"]
    SESSION_SECRET = get_secret(os.environ["SESSION_TOKEN_SECRET_ARN"]["RsvpJwtSecret"])
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
    JwtGenerator(SESSION_SECRET, 15, "minutes")
)

#choose controller based on CONTROLLER environment variable
controller: "Controller" = globals()[f"{CONTROLLER}_controller"]

def lambda_handler(event, _):
    log.info("WeddingRsvp common lambda entrypoint reached")
    return {
        "get": _handle_get,
        "post": _handle_post,
    }[event["httpMethod"].lower()](event)


def _handle_get(event):
    log.info("Handling GET request")
    #TODO parse QS
    #TODO use environment variables to choose controller
    return controller.get({})


def _handle_post(event):
    log.info("Handling POST request")
    return controller.post(parse_qs(event['body']))
