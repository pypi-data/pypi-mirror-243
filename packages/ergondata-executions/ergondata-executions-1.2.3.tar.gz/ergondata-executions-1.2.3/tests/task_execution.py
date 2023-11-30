import os
from dotenv import load_dotenv

from ergondata_executions.controllers.auth.controller import AuthController
from ergondata_executions.controllers.auth.interfaces import AuthRequestPayload

from ergondata_executions.controllers.task_execution.controller import TaskExecutionController
from ergondata_executions.controllers.task_execution.interfaces import *

from ergondata_executions.controllers.queue_item.controller import QueueItemController
from ergondata_executions.controllers.queue_item.interfaces import *

from ergondata_executions.controllers.task_execution_log.controller import TaskExecutionLogController
from ergondata_executions.controllers.task_execution_log.interfaces import *

load_dotenv()
'''
auth = AuthRequestPayload(
    username=os.getenv('WORKER_API_USERNAME'),
    password=os.getenv('WORKER_API_PASSWORD'),
    client_id=os.getenv('WORKER_API_CLIENT_ID')
)

api_client = AuthController(auth=auth, timeout=1000)
controller = TaskExecutionController(api_client=api_client)

create_task_execution_request = CreateTaskExecutionRequestPayload(
    task_id="058537b1-59ae-44f6-b4cc-bd3c14849158",
    dev_mode=True
)
create_task_execution_response = controller.create_task_execution(create_task_execution_request)

if create_task_execution_response.status == "error":
    reset_task_execution_response = controller.reset_task_execution()
    create_task_execution_response = controller.create_task_execution(create_task_execution_request)

qi_controller = QueueItemController(api_client=api_client)

for i in range(0, 10):
    create_queue_item_request = CreateQueueItemRequestPayload(
        external_id="daniel.vossos@ergondata.com.br-xxx",
        queue_id="27b5213b-84eb-4e43-a935-6a261105c520",
        payload=[
            {"nome": "Daniel", "email": "daniel.vossos@ergondata.com.br"},
            {"nome": "Daniel", "email": "daniel.vossos@ergondata.com.br"},
            {"nome": "Daniel", "email": "daniel.vossos@ergondata.com.br"}
        ],
        processing_status_message="Teste"
    )
    create_queue_item_response = qi_controller.create_queue_item(create_queue_item_request)

update_task_execution_request = UpdateTaskExecutionRequestPayload(
    task_execution_status_id="success"
)
controller.update_task_execution(params=update_task_execution_request)
'''

auth = AuthRequestPayload(
    username=os.getenv('WORKER_API_USERNAME'),
    password=os.getenv('WORKER_API_PASSWORD'),
    client_id=os.getenv('WORKER_API_CLIENT_ID')
)

api_client = AuthController(auth=auth, timeout=1000)
tke_controller = TaskExecutionController(api_client=api_client)

create_task_execution_request = CreateTaskExecutionRequestPayload(
    task_id="c2f8e19e-fac1-4f48-8292-e2861cb67b87",
    dev_mode=True
)
create_task_execution_response = tke_controller.create_task_execution(create_task_execution_request)
tke_log_controller = TaskExecutionLogController(api_client=api_client)

if create_task_execution_response.status == "error":
    reset_task_execution_response = tke_controller.reset_task_execution()
    create_task_execution_response = tke_controller.create_task_execution(create_task_execution_request)

qi_controller = QueueItemController(api_client=api_client)


while True:

    create_task_execution_log_request = CreateTaskExecutionLogRequestPayload(
        log_type="info",
        log_message="Getting next queue item"
    )
    create_task_execution_log_response = tke_log_controller.create_task_execution_log(create_task_execution_log_request)

    get_queue_item_request = GetQueueItemRequestPayload(
        queue_id="27b5213b-84eb-4e43-a935-6a261105c520"
    )

    get_queue_item_response = qi_controller.get_queue_item(get_queue_item_request)

    if get_queue_item_response.status == "error":
        reset_queue_item_response = qi_controller.reset_queue_item()
        get_queue_item_response = qi_controller.get_queue_item(get_queue_item_request)

    if get_queue_item_response.data:
        update_queue_item_request = UpdateQueueItemRequestPayload(
            queue_item_id=get_queue_item_response.data.id,
            queue_item_processing_status_message="CASO TBE: 2443943. Motorista: João da Silva",
            queue_item_processing_exception_id="61d8241a-58b7-11ee-8c99-0242ac120002"
        )

        create_task_execution_log_request = CreateTaskExecutionLogRequestPayload(
            log_type="info",
            log_message="Updating queue item"
        )
        create_task_execution_log_response = tke_log_controller.create_task_execution_log(create_task_execution_log_request)
        update_queue_item_response = qi_controller.update_queue_item(update_queue_item_request)
    else:
        break

update_task_execution_request = UpdateTaskExecutionRequestPayload(
    task_execution_status_id="success"
)
update_task_execution_response = tke_controller.update_task_execution(update_task_execution_request)


'''
auth = AuthRequestPayload(
    username="",
    password=""
)

api_client = AuthController(auth=auth, timeout=1000)
tke_controller = TaskExecutionController(api_client=api_client)
qi_controller = QueueItemController(api_client=api_client)

get_queue_items_request = GetQueueItemsRequestPayload(
    queue_id="39208da3-5482-4c57-8698-4119d8749d2d",
    created_at_lte="2023-09-19T11:00:00.000-03:00"
)
get_queue_items_response = qi_controller.get_queue_items(get_queue_items_request)
print(get_queue_items_response)

'''
'''
auth = AuthRequestPayload(
    username="",
    password=""
)
api_client = AuthController(auth=auth, timeout=1000)
tke_controller = TaskExecutionController(api_client=api_client)
tke_log_controller = TaskExecutionLogController(api_client=api_client)

create_task_execution_request = CreateTaskExecutionRequestPayload(
    task_id="6a3ca202-d35c-42fc-b89f-6cf1390a7618",
    dev_mode=True
)
create_task_execution_response = tke_controller.create_task_execution(create_task_execution_request)

if create_task_execution_response.status == "error":
    reset_task_execution_response = tke_controller.reset_task_execution()
    create_task_execution_response = tke_controller.create_task_execution(create_task_execution_request)

tke_log_controller = TaskExecutionLogController(api_client=api_client)

create_task_execution_log_request = CreateTaskExecutionLogRequestPayload(
    log_type="error",
    log_message="Teste"
)
create_task_execution_log_response = tke_log_controller.create_task_execution_log(create_task_execution_log_request)

update_task_execution_request = UpdateTaskExecutionRequestPayload(
    task_execution_status_id="success"
)
update_task_execution_response = tke_controller.update_task_execution(update_task_execution_request)
'''
'''auth = AuthRequestPayload(
    username="",
    password=""
)
api_client = AuthController(auth=auth, timeout=1000)
tke_log_controller = TaskExecutionLogController(api_client=api_client)

get_task_execution_logs_request = GetTaskExecutionLogsRequestPayload(
    task_id="6a3ca202-d35c-42fc-b89f-6cf1390a7618"
)
get_task_execution_logs_response = tke_log_controller.get_task_execution_logs(get_task_execution_logs_request)'''