import json
from datetime import datetime, timedelta, timezone
import logging
import os

from jwt import (
    JWT,
    jwk_from_dict,
    jwk_from_pem,
)
from jwt.jwk import OctetJWK
from jwt.utils import get_int_from_datetime

log = logging.getLogger(__name__)
log.setLevel(getattr(logging, os.environ.get("LOG_LEVEL", "info").upper()))


class JwtValidator:
    _ISSUER: str = "https://rsvp.adriandmikejones.com/"
    _jwt_secret: OctetJWK
    def __init__(self, jwt_secret: bytes):
        self._jwt_secret = OctetJWK(jwt_secret)

    def is_valid_jwt(self, jwt: str) -> bool:
        try:
            message_received: dict = self._decode_jwt(jwt)
            assert message_received["iss"] == self._ISSUER
            log.info("JWT valid")
            return True
        except Exception as exception:
            log.warn("Invalid JWT")
            log.warn(exception)

        return False

    def get_sub(self, jwt:str) -> str:
        return self._decode_jwt(jwt)["sub"]    
    
    def _decode_jwt(self, jwt: str) -> dict:
        return JWT().decode(jwt, self._jwt_secret, do_time_check=True)
