import requests
from ergondata_executions.controllers.task_execution.interfaces import *
from ergondata_executions.controllers.auth.controller import AuthController


class TaskExecutionController:

    CREATE_TASK_EXECUTION_URL = "create/database/process/task/execution"
    RESET_TASK_EXECUTION_URL = "reset/database/process/task/execution"
    GET_TASK_EXECUTIONS_URL = "get/database/process/task/{0}/executions?"
    UPDATE_TASK_EXECUTION_URL = "update/database/process/task/execution"

    def __init__(self, api_client: AuthController):
        self.api_client = api_client


    def create_task_execution(self, params: CreateTaskExecutionRequestPayload) -> CreateTaskExecutionResponsePayload:

        self.api_client.log_info(f"Creating task_execution for task id{params.task_id}.")

        try:

            res = requests.post(
                url=f"{self.api_client.ROOT_URL}{self.CREATE_TASK_EXECUTION_URL}",
                json=params.model_dump(),
                headers=self.api_client.auth_header,
                timeout=self.api_client.timeout
            )

            response_payload = CreateTaskExecutionResponsePayload(**res.json())

            if response_payload.execution_token:
                self.api_client.execution_token = response_payload.execution_token

            if res.status_code == 200:
                self.api_client.log_info(response_payload)
            else:
                self.api_client.log_error(response_payload)
            return response_payload

        except BaseException as e:

            self.api_client.log_error(f"Failed to create task_execution{e}.")

            response_payload = CreateTaskExecutionResponsePayload(
                status="error",
                message=str(e)
            )

            return response_payload

    def get_task_executions(self, params: GetTaskExecutionsRequestPayload) -> GetTaskExecutionsResponsePayload:

        self.api_client.log_info(f"Getting task_executions for task {params.task_id}")

        try:

            get_task_url = self.GET_TASK_EXECUTIONS_URL.format(params.task_id)

            get_task_url = get_task_url + f'created_at_lt={params.created_at_lt}&' if params.created_at_lt else get_task_url
            get_task_url = get_task_url + f'created_at_lte={params.created_at_lte}&' if params.created_at_lte else get_task_url
            get_task_url = get_task_url + f'created_at_gt={params.created_at_gt}&' if params.created_at_gt else get_task_url
            get_task_url = get_task_url + f'created_at_gte={params.created_at_gte}&' if params.created_at_gte else get_task_url
            get_task_url = get_task_url + f'finished_at_lte={params.finished_at_lte}&' if params.finished_at_lte else get_task_url
            get_task_url = get_task_url + f'finished_at_lt={params.finished_at_lt}&' if params.finished_at_lt else get_task_url
            get_task_url = get_task_url + f'finished_at_gt={params.finished_at_gt}&' if params.finished_at_gt else get_task_url
            get_task_url = get_task_url + f'finished_at_gte={params.finished_at_gte}&' if params.finished_at_gte else get_task_url
            get_task_url = get_task_url + f'processing_status_id={params.processing_status_id}&' if params.processing_status_id else get_task_url
            get_task_url = get_task_url + f'processing_exception_id={params.processing_exception_id}&' if params.processing_exception_id else get_task_url

            res = requests.get(
                url=f"{self.api_client.ROOT_URL}{get_task_url}",
                headers=self.api_client.auth_header,
                timeout=self.api_client.timeout
            )
            response_payload = GetTaskExecutionsResponsePayload(**res.json())

            if res.status_code == 200:
                self.api_client.log_info(response_payload)
            else:
                self.api_client.log_error(response_payload)
            return response_payload

        except BaseException as e:

            self.api_client.log_error(f"Failed to get task_executions {e}.")

            response_payload = GetTaskExecutionsResponsePayload(
                status="error",
                message=str(e)
            )

            return response_payload

    def update_task_execution(self, params: UpdateTaskExecutionRequestPayload) -> APIBaseResponse:

        self.api_client.log_info(f"Updating task_execution status {params.task_execution_status_id}")

        try:

            res = requests.put(
                url=f"{self.api_client.ROOT_URL}{self.UPDATE_TASK_EXECUTION_URL}",
                json=params.model_dump(),
                headers=self.api_client.exec_header,
                timeout=self.api_client.timeout
            )

            response_payload = APIBaseResponse(**res.json())
            if res.status_code == 200:
                self.api_client.log_info(response_payload)
            else:
                self.api_client.log_error(response_payload)
            return response_payload

        except BaseException as e:

            self.api_client.log_error(f"Failed to update task_execution {e}.")

            response_payload = APIBaseResponse(
                status="error",
                message=str(e)
            )

            return response_payload

    def reset_task_execution(self) -> APIBaseResponse:

        self.api_client.log_info(f"Resetting task execution")

        try:
            
            res = requests.post(
                url=f"{self.api_client.ROOT_URL}{self.RESET_TASK_EXECUTION_URL}",
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

            self.api_client.log_error(f"Failed to reset task_execution {e}.")

            response_payload = APIBaseResponse(
                status="error",
                message=str(e)
            )

            return response_payload
