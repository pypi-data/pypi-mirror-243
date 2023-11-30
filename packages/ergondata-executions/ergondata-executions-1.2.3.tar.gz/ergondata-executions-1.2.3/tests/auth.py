import os
from dotenv import load_dotenv

from ergondata_executions.controllers.auth.controller import AuthController
from ergondata_executions.controllers.auth.interfaces import *

load_dotenv()

auth_req = AuthRequestPayload(
    username=os.getenv('WORKER_API_USERNAME'),
    password=os.getenv('WORKER_API_PASSWORD'),
    client_id=os.getenv('WORKER_API_CLIENT_ID')
)
auth_controller = AuthController(auth_req, enable_logs=True, timeout=1000)

