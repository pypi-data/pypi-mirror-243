import requests
from ergondata_executions.controllers.task.interfaces import *
from ergondata_executions.controllers.auth.controller import AuthController
from ergondata_executions.controllers.task_processing_exception.controller import TaskProcessingExceptionController


class TaskController(TaskProcessingExceptionController):

    CREATE_TASK_URL = "create/database/process/task"
    DELETE_TASK_URL = "delete/database/process/task/{0}"
    GET_TASKS_URL = "get/database/process/{0}/tasks"
    UPDATE_TASK_URL = "update/database/process/task"

    def __init__(self, api_client: AuthController):
        self.api_client = api_client
        super(TaskController, self).__init__(api_client=api_client)

    def create_task(self, params: CreateTaskRequestPayload) -> CreateTaskResponsePayload:

        self.api_client.log_info(f"Creating task {params.task_name}.")

        try:

            res = requests.post(
                url=f"{self.api_client.ROOT_URL}{self.CREATE_TASK_URL}",
                json=params.model_dump(),
                headers=self.api_client.auth_header,
                timeout=self.api_client.timeout
            )

            response_payload = CreateTaskResponsePayload(**res.json())
            if res.status_code == 200:
                self.api_client.log_info(response_payload)
            else:
                self.api_client.log_error(response_payload)

            return response_payload

        except BaseException as e:

            self.api_client.log_error(f"Failed to create task{e}.")

            response_payload = CreateTaskResponsePayload(
                status="error",
                message=str(e)
            )

            return response_payload

    def delete_task(self, params: DeleteTaskRequestPayload) -> APIBaseResponse:

        self.api_client.log_info(f"Deleting task id {params.task_id}")

        try:

            res = requests.delete(
                url=f"{self.api_client.ROOT_URL}{self.DELETE_TASK_URL.format(params.task_id)}",
                json=params.model_dump(),
                headers=self.api_client.auth_header,
                timeout=self.api_client.timeout
            )

            response_payload = APIBaseResponse(**res.json())
            if res.status_code == 200:
                self.api_client.log_info(response_payload)
            else:
                self.api_client.log_error(response_payload)

            return response_payload

        except BaseException as e:

            self.api_client.log_error(f"Failed to delete task{e}.")

            response_payload = CreateTaskResponsePayload(
                status="error",
                message=str(e)
            )

            return response_payload

    def get_tasks(self, params: GetTasksRequestPayload) -> GetTasksResponsePayload:

        self.api_client.log_info(f"Getting tasks for process {params.process_id}")

        try:

            res = requests.get(
                url=f"{self.api_client.ROOT_URL}{self.GET_TASKS_URL.format(params.process_id)}",
                headers=self.api_client.auth_header,
                timeout=self.api_client.timeout
            )

            response_payload = GetTasksResponsePayload(**res.json())
            if res.status_code == 200:
                self.api_client.log_info(response_payload)
            else:
                self.api_client.log_error(response_payload)

            return response_payload
                
        except BaseException as e:

            self.api_client.log_error(f"Failed to get tasks {e}.")
            response_payload = GetTasksResponsePayload(
                status="error",
                message=str(e)
            )

            return response_payload

    def update_tasks(self, params: UpdateTaskRequestPayload) -> APIBaseResponse:

        self.api_client.log_info(f"Updating task id {params.task_id}")

        try:

            res = requests.put(
                url=f"{self.api_client.ROOT_URL}{self.UPDATE_TASK_URL}",
                json=params.model_dump(),
                headers=self.api_client.auth_header,
                timeout=self.api_client.timeout
            )

            response_payload = APIBaseResponse(**res.json())
            if res.status_code == 200:
                self.api_client.log_info(response_payload)
            else:
                self.api_client.log_error(response_payload)
            return response_payload

        except BaseException as e:

            self.api_client.log_error(f"Failed to update task {e}.")

            response_payload = APIBaseResponse(
                status="error",
                message=str(e)
            )

            return response_payload
