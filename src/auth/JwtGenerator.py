class JwtGenerator:
    _jwt_secret: str
    
    def __init__(self, jwt_secret: str):
        self._jwt_secret = jwt_secret

    def new_jwt() -> str:
        raise NotImplemented()
