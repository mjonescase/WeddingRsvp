import json
import os
from typing import Dict, List
from urllib.parse import parse_qs

from auth.PasscodeValidator import PasscodeValidator
from auth.JwtGenerator import JwtGenerator
from controllers.LoginController import LoginController
from secret_dao import get_secret

HASHED_PASSCODE = "not set"
JWT_SECRET = "not set"
if not os.environ.get("IS_LOCAL"):
    HASHED_PASSCODE = get_secret(os.environ["PASSCODE_ARN"])["RsvpPassword"]
    JWT_SECRET = get_secret(os.environ["JWT_SECRET_ARN"])["RsvpJwtSecret"]
    
SURVEY_URI = 'https://docs.google.com/forms/d/e/1FAIpQLSdBwK3Zc9KtIjpX8J5EvTcYj-PAWrQR2K7m3qwTdYZL7q0GIg/viewform?usp=sf_link'

passcode_validator: PasscodeValidator = PasscodeValidator(HASHED_PASSCODE)
jwt_generator: JwtGenerator = JwtGenerator(JWT_SECRET)
login_controller: LoginController = LoginController(
    passcode_validator,
    jwt_generator,
    SURVEY_URI
)


def lambda_handler(event, _):
    return {
        'GET': _handle_get,
        'POST': _handle_post,
    }[event['httpMethod']](event)


def _handle_get(event):
    #TODO parse QS
    #TODO use environment variables to choose controller
    return login_controller.get({})


def _handle_post(event):
    return login_controller.post(parse_qs(event['body']))
