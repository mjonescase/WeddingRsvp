class JwtValidator:
    def __init__(self, jwt_secret: str):
        self._jwt_secret = jwt_secret

    def is_valid_jwt(jwt: str) -> bool:
        raise NotImplemented()
