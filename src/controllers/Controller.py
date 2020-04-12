from datetime import datetime
from typing import Dict, List


class Controller:
    def get(
            self,
            query_string: Dict[str, str],
            headers: Dict[str, str],
            multi_value_headers: Dict[str, List[str]]
    ) -> dict:
        raise NotImplemented()

    def post(
            self,
            form: Dict[str, List[str]],
            headers: Dict[str, str],
            multi_value_headers: Dict[str, List[str]]
    ) -> dict:
        raise NotImplemented()
        
    @classmethod
    def respond_with_html(
            cls,
            body: str,
            status_code: int=200,
            set_cookie_header: str=None) -> dict:
        headers: dict = {
            'Content-Type': 'text/html',    
        }
        if set_cookie_header is not None:
            headers['Set-Cookie'] = set_cookie_header
        
        return {
            'statusCode': status_code,
            'body': body,
            'headers': headers
        }

    @classmethod
    def redirect(cls, location: str) -> dict:
        return {
            'statusCode': 301,
            'headers': {
                'Location': location
            }
        }

    def build_session_secret(self, user_agent: str) -> str:
        return ",".join([
            datetime.strftime(datetime.now(), "%Y-%m-%dT%H:%M:%S.%f"),
            user_agent
        ])

    def build_session_cookie(
            self,
            session_token: str,
            duration: "datetime.timedelta"
    ) -> str:
        return ";".join([
            "session={0}",
            "Domain={1}",
            "Path={2}",
            "Max-Age={3}",
            "SameSite=Lax",
            "HttpOnly",
            "Secure"
        ]).format(
            session_token,
            "rsvp.adriandmikejones.com",
            "/authenticate",
            duration.seconds
        )
    
