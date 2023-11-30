import requests
from ergondata_executions.controllers.auth.interfaces import *
from ergondata_executions.api_logger import APILogger


class AuthController(APILogger):

    ROOT_URL = "https://executions.ergondata.com.br/api/"
    # ROOT_URL = "http://127.0.0.1:8000/api/"
    AUTH_URL = "auth"

    def __init__(self, auth: AuthRequestPayload, timeout: int = 10, enable_logs: bool = True):
        super(AuthController, self).__init__(enable_logs=enable_logs)
        self.auth = auth
        self.timeout = timeout
        self.auth_token = AuthController.__authenticate(self=self).token
        self.execution_token = None

    @property
    def auth_header(self):
        return {"Authorization": f"Bearer {self.auth_token}"}

    @property
    def exec_header(self):
        return {"Authorization": f"Bearer {self.execution_token}"}

    def __authenticate(self) -> AuthResponsePayload:

        try:

            self.log_info(f"Authenticating user { self.auth.username }")
            res = requests.post(
                url=f"{AuthController.ROOT_URL}{AuthController.AUTH_URL}",
                json=self.auth.model_dump(),
                timeout=self.timeout
            )
            response = AuthResponsePayload(**res.json())

            if res.status_code == 200:
                self.log_info(response)
            else:
                self.log_error(response.message)

            return response

        except BaseException as e:

            self.log_error(f"Failed to authenticate user. {e}")
            response = AuthResponsePayload(
                status="error",
                message=str(e)
            )
            return response


