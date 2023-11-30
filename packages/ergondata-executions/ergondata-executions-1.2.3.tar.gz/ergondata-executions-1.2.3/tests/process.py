import os

from ergondata_executions.controllers.auth.controller import AuthController
from ergondata_executions.controllers.auth.interfaces import AuthRequestPayload

from ergondata_executions.controllers.process.controller import ProcessController
from ergondata_executions.controllers.process.interfaces import *

auth = AuthRequestPayload(
    username=os.getenv('CLIENT_OWNER_API_USERNAME'),
    password=os.getenv('CLIENT_OWNER_API_PASSWORD')
)

api_client = AuthController(auth=auth, logging=True, timeout=20)
controller = ProcessController(api_client)

create_process_request = CreateProcessRequestPayload(
    database_id="2cfef6f3-22c6-4400-bb13-7d95850f4bef",
    process_title="JJ-Mendes",
    process_description="Este processo é divido em três task para efetuar o processo do jj mendes até o final."
)
create_process_response = controller.create_process(params=create_process_request)

delete_process_request = DeleteProcessRequestPayload(
    process_id="0cce1515-c965-42f7-a1d0-c360e7875bb9"
)
delete_process_response = controller.delete_process(params=delete_process_request)

get_processes_request = GetProcessesRequestPayload(
    database_id="2cfef6f3-22c6-4400-bb13-7d95850f4bef"
)
get_processes_response = controller.get_processes(params=get_processes_request)