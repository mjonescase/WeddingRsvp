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


class JwtGenerator:
    _ALG: str = "HS256" #symmetric/shared secret
    _jwt_secret: OctetJWK
    _duration_amount: int
    _duration_units: str #hours, minutes or seconds
    
    def __init__(
        self,
        jwt_secret: str,
        duration_amount: int,
        duration_units: str
    ):
        self._jwt_secret = OctetJWK(jwt_secret)
        self._duration_amount = duration_amount
        if duration_units not in { "hours", "minutes", "seconds" }:
            error_message: str = f"Invalid time unit string: {duration_units}"
            log.error(error_message)
            raise ValueError(error_message)

        self._duration_units = duration_units

    def build_jwt(self) -> str:
        utc_now: int = datetime.now(timezone.utc)
        return JWT().encode(
            {
                'iss': 'https://rsvp.adriandmikejones.com/',
                'sub': 'guest',
                'iat': get_int_from_datetime(utc_now),
                'exp': get_int_from_datetime(utc_now + timedelta(**{self._duration_units: self._duration_amount})),
            },
            self._jwt_secret,
            alg=self._ALG,
        )
