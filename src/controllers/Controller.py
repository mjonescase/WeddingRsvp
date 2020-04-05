from typing import Dict, List


class Controller:
    def get(self, query_string: Dict[str, str]) -> dict:
        raise NotImplemented()

    def post(self, form: Dict[str, List[str]]) -> dict:
        raise NotImplemented()
        
    @classmethod
    def respond_with_html(
            cls,
            body: str,
            status_code: int=200,
            authorization_header: str=None) -> dict:
        headers: dict = {
            'Content-Type': 'text/html',    
        }
        if authorization_header is not None:
            headers['Authorization'] = authorization_header
        
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
