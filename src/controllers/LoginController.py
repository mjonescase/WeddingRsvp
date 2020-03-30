from .Controller import Controller
from views.LoginView import LoginView

class LoginController(Controller):
    _view = LoginView
    _passcode_validator: "..auth.PasscodeValidator"
    _jwt_generator: "..auth.JwtGenerator"
    _survey_uri: str
    
    def __init__(
            self,
            passcode_validator: "..auth.PasscodeValidator",
            jwt_generator: "..auth.JwtGenerator",
            survey_uri: str
    ):
        self._passcode_validator = passcode_validator
        self._jwt_generator = jwt_generator
        self._survey_uri = survey_uri

    def get(self, query_string: dict) -> dict:
        return self.__class__.respond_with_html(LoginView.get_html())

    def post(self, form: dict) -> dict:
        if self._passcode_validator.is_valid_passcode(form["passcode"][0]):
            return self.__class__.redirect(self._survey_uri)

        return self.__class__.respond_with_html(LoginView.get_html(False))
