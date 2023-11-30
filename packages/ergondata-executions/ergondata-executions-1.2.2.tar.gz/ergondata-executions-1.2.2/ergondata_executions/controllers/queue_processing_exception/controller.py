import requests
from ergondata_executions.controllers.auth.controller import AuthController
from ergondata_executions.controllers.queue_processing_exception.interfaces import *


class QueueProcessingExceptionController:

    CREATE_QUEUE_PROCESSING_EXCEPTION_URL = "create/database/process/queue/exception"
    DELETE_QUEUE_PROCESSING_EXCEPTION_URL = "delete/database/process/queue/exception/{0}"
    GET_QUEUE_PROCESSING_EXCEPTIONS_URL = "get/database/process/queue/{0}/exceptions"
    UPDATE_QUEUE_PROCESSING_EXCEPTION_URL = "update/database/process/queue/exception"

    def __init__(self, api_client: AuthController):
        self.api_client = api_client

    def create_queue_processing_exception(self, params: CreateQueueProcessingExceptionRequestPayload) -> CreateQueueProcessingExceptionResponsePayload:

        self.api_client.log_info(f"Creating queue exception for queue id {params.queue_id}.")

        try:

            res = requests.post(
                url=f"{self.api_client.ROOT_URL}{self.CREATE_QUEUE_PROCESSING_EXCEPTION_URL}",
                json=params.model_dump(),
                headers=self.api_client.auth_header,
                timeout=self.api_client.timeout
            )

            response_payload = CreateQueueProcessingExceptionResponsePayload(**res.json())
            if res.status_code == 200:
                self.api_client.log_info(response_payload)
            else:
                self.api_client.log_error(response_payload)

            return response_payload

        except BaseException as e:

            self.api_client.log_error(f"Failed to create queue processing exception {e}.")

            response_payload = CreateQueueProcessingExceptionResponsePayload(
                status="error",
                message=str(e)
            )

            return response_payload

    def delete_queue_processing_exception(self, params: DeleteQueueProcessingExceptionRequestPayload) -> APIBaseResponse:

        self.api_client.log_info(f"Deleting queue exception {params.queue_processing_exception_id}.")

        try:

            res = requests.delete(
                url=f"{self.api_client.ROOT_URL}{self.DELETE_QUEUE_PROCESSING_EXCEPTION_URL.format(params.queue_processing_exception_id)}",
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

            self.api_client.log_error(f"Failed to delete queue processing exception {e}.")

            response_payload = CreateQueueProcessingExceptionResponsePayload(
                status="error",
                message=str(e)
            )

            return response_payload


    def get_queue_processing_exceptions(self, params: GetQueueProcessingExceptionsRequestPayload) -> GetQueueProcessingExceptionsResponsePayload:

        self.api_client.log_info(f"Getting queue exceptions for queue id {params.queue_id}.")

        try:

            res = requests.get(
                url=f"{self.api_client.ROOT_URL}{self.GET_QUEUE_PROCESSING_EXCEPTIONS_URL.format(params.queue_id)}",
                headers=self.api_client.auth_header,
                timeout=self.api_client.timeout
            )

            response_payload = GetQueueProcessingExceptionsResponsePayload(**res.json())
            if res.status_code == 200:
                self.api_client.log_info(response_payload)
            else:
                self.api_client.log_error(response_payload)

            return response_payload

        except BaseException as e:

            self.api_client.log_error(f"Failed get queue exceptions {e}.")

            response_payload = GetQueueProcessingExceptionsResponsePayload(
                status="error",
                message=str(e)
            )

            return response_payload

    def update_queue_processing_exceptions(self, params: UpdateQueueProcessingExceptionRequestPayload) -> APIBaseResponse:

        self.api_client.log_info(f"Updating queue exception {params.queue_processing_exception_id}.")

        try:

            res = requests.put(
                url=f"{self.api_client.ROOT_URL}{self.UPDATE_QUEUE_PROCESSING_EXCEPTION_URL}",
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

            self.api_client.log_error(f"Failed to update queue processing exception {e}.")

            response_payload = APIBaseResponse(
                status="error",
                message=str(e)
            )

            return response_payload

