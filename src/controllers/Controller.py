from typing import Dict, List


class Controller:
    def get(self, query_string: Dict[str, str]) -> dict:
        raise NotImplemented()

    def post(self, form: Dict[str, List[str]]) -> dict:
        raise NotImplemented()
        
    @classmethod
    def respond_with_html(cls, body: str, status_code: int=200) -> dict:
        return {
            'statusCode': status_code,
            'body': body,
            'headers': {
                'Content-Type': 'text/html'
            }
        }

    @classmethod
    def redirect(cls, location: str) -> dict:
        return {
            'statusCode': 301,
            'headers': {
                'Location': location
            }
        }
