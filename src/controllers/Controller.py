from typing import Dict, List


class Controller:
    def get(self, query_string: Dict[str, str]) -> dict:
        raise NotImplemented()

    def post(self, form: Dict[str, List[str]], headers: Dict) -> dict:
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
