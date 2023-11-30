import os
from dotenv import load_dotenv

from ergondata_executions.controllers.auth.controller import AuthController
from ergondata_executions.controllers.worker.controller import WorkerController
from ergondata_executions.controllers.auth.interfaces import AuthRequestPayload
from ergondata_executions.controllers.worker.interfaces import *


load_dotenv()

auth = AuthRequestPayload(
    username=os.getenv('CLIENT_OWNER_API_USERNAME'),
    password=os.getenv('CLIENT_OWNER_API_PASSWORD'),
    client_id=os.getenv('CLIENT_OWNER_API_CLIENT_ID')
)

api_client = AuthController(auth=auth, logging=True, timeout=20)
controller = WorkerController(api_client=api_client)

create_worker_request = CreateWorkerRequestPayload(worker_first_name="worker-01")
# create_worker_response = controller.create_worker(params=create_worker_request)

'''
delete_worker_request = DeleteWorkerRequestPayload(
    worker_id=create_worker_response.worker_id
)
delete_worker_response = controller.delete_worker(params=delete_worker_request)
'''

get_workers_request = controller.get_workers()
