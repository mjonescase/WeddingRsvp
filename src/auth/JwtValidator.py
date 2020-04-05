import json
from datetime import datetime, timedelta, timezone
import logging
import os

from jwt import (
    JWT,
    jwk_from_dict,
    jwk_from_pem,
)
from jwt.utils import get_int_from_datetime

log = logging.getLogger(__name__)
log.setLevel(getattr(logging, os.environ.get("LOG_LEVEL", "info").upper()))


class JwtValidator:
    _ISSUER: str = "https://rsvp.adriandmikejones.com/"
    _SUBJECT: str = "guest"
    _jwt_secret: str
    def __init__(self, jwt_secret: str):
        self._jwt_secret = jwt_secret

    def is_valid_jwt(jwt: str) -> bool:
        try:
            message_received: str = JWT().decode(
                jwt,
                self._jwt_secret,
                do_time_check=True
            )
            assert message_received["iss"] == self._ISSUER
            assert message_received["sub"] == self._SUBJECT
            log.info("JWT valid")
            return True
        except Exception as exception:
            log.warn("Invalid JWT")
            log.warn(exception)

        return False   
