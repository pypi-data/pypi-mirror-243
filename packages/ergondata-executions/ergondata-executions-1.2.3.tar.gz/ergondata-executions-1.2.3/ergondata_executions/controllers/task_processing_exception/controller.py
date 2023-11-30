import requests
from ergondata_executions.controllers.auth.controller import AuthController
from ergondata_executions.controllers.task_processing_exception.interfaces import *


class TaskProcessingExceptionController:

    CREATE_TASK_PROCESSING_EXCEPTION_URL = "create/database/process/task/exception"
    DELETE_TASK_PROCESSING_EXCEPTION_URL = "delete/database/process/task/exception/{0}"
    GET_TASK_PROCESSING_EXCEPTIONS_URL = "get/database/process/task/{0}/exceptions"
    UPDATE_TASK_PROCESSING_EXCEPTION_URL = "update/database/process/task/exception"

    def __init__(self, api_client: AuthController):
        self.api_client = api_client

    def create_task_processing_exception(self, params: CreateTaskProcessingExceptionRequestPayload) -> CreateTaskProcessingExceptionResponsePayload:

        self.api_client.log_info(f"Creating task exception for task id {params.task_id}.")

        try:

            res = requests.post(
                url=f"{self.api_client.ROOT_URL}{self.CREATE_TASK_PROCESSING_EXCEPTION_URL}",
                json=params.model_dump(),
                headers=self.api_client.auth_header,
                timeout=self.api_client.timeout
            )

            response_payload = CreateTaskProcessingExceptionResponsePayload(**res.json())
            if res.status_code == 200:
                self.api_client.log_info(response_payload)
            else:
                self.api_client.log_error(response_payload)

            return response_payload

        except BaseException as e:

            self.api_client.log_error(f"Failed to create task processing exception {e}.")

            response_payload = CreateTaskProcessingExceptionResponsePayload(
                status="error",
                message=str(e)
            )

            return response_payload

    def delete_task_processing_exception(self, params: DeleteTaskProcessingExceptionRequestPayload) -> APIBaseResponse:

        self.api_client.log_info(f"Deleting task exception {params.task_processing_exception_id}.")

        try:

            res = requests.delete(
                url=f"{self.api_client.ROOT_URL}{self.DELETE_TASK_PROCESSING_EXCEPTION_URL.format(params.task_processing_exception_id)}",
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

            self.api_client.log_error(f"Failed to delete task processing exception {e}.")

            response_payload = CreateTaskProcessingExceptionResponsePayload(
                status="error",
                message=str(e)
            )

            return response_payload


    def get_task_processing_exceptions(self, params: GetTaskProcessingExceptionsRequestPayload) -> GetTaskProcessingExceptionsResponsePayload:

        self.api_client.log_info(f"Getting task exceptions for task id {params.task_id}.")

        try:

            res = requests.get(
                url=f"{self.api_client.ROOT_URL}{self.GET_TASK_PROCESSING_EXCEPTIONS_URL.format(params.task_id)}",
                headers=self.api_client.auth_header,
                timeout=self.api_client.timeout
            )

            response_payload = GetTaskProcessingExceptionsResponsePayload(**res.json())
            if res.status_code == 200:
                self.api_client.log_info(response_payload)
            else:
                self.api_client.log_error(response_payload)

            return response_payload

        except BaseException as e:

            self.api_client.log_error(f"Failed get task exceptions {e}.")

            response_payload = GetTaskProcessingExceptionsResponsePayload(
                status="error",
                message=str(e)
            )

            return response_payload

    def update_task_processing_exceptions(self, params: UpdateTaskProcessingExceptionRequestPayload) -> APIBaseResponse:

        self.api_client.log_info(f"Updating task exception {params.task_processing_exception_id}.")

        try:

            res = requests.put(
                url=f"{self.api_client.ROOT_URL}{self.UPDATE_TASK_PROCESSING_EXCEPTION_URL}",
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

            self.api_client.log_error(f"Failed to update task processing exception {e}.")

            response_payload = APIBaseResponse(
                status="error",
                message=str(e)
            )

            return response_payload
