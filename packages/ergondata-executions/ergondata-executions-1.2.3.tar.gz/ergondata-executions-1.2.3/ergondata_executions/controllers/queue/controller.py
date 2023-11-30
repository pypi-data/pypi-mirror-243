import requests
from ergondata_executions.controllers.queue.interfaces import *
from ergondata_executions.controllers.auth.controller import AuthController


class QueueController:

    CREATE_QUEUE_URL = "create/database/process/queue"
    DELETE_QUEUE_URL = "delete/database/process/queue/{0}"
    GET_QUEUES_URL = "get/database/process/{0}/queues"
    UPDATE_QUEUE_URL = "update/database/process/queue"

    def __init__(self, api_client: AuthController):
        self.api_client = api_client

    def create_queue(self, params: CreateQueueRequestPayload) -> CreateQueueResponsePayload:

        self.api_client.log_info(f"Creating queue {params.queue_name}.")

        try:

            res = requests.post(
                url=f"{self.api_client.ROOT_URL}{self.CREATE_QUEUE_URL}",
                json=params.model_dump(),
                headers=self.api_client.auth_header,
                timeout=self.api_client.timeout
            )

            response_payload = CreateQueueResponsePayload(**res.json())
            if res.status_code == 200:
                self.api_client.log_info(response_payload)
            else:
                self.api_client.log_error(response_payload)
            return response_payload

        except BaseException as e:

            self.api_client.log_error(f"Failed to create queue{e}.")

            response_payload = CreateQueueResponsePayload(
                status="error",
                message=str(e)
            )

            return response_payload

    def delete_queue(self, params: DeleteQueueRequestPayload) -> APIBaseResponse:

        self.api_client.log_info(f"Deleting queue id {params.queue_id}")

        try:

            res = requests.delete(
                url=f"{self.api_client.ROOT_URL}{self.DELETE_QUEUE_URL.format(params.queue_id)}",
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

            self.api_client.log_error(f"Failed to delete queue{e}.")

            response_payload = CreateQueueResponsePayload(
                status="error",
                message=str(e)
            )

            return response_payload

    def get_queues(self, params: GetQueuesRequestPayload) -> GetQueuesResponsePayload:

        self.api_client.log_info("Getting queues for process {params.process_id}")

        try:

            res = requests.get(
                url=f"{self.api_client.ROOT_URL}{self.GET_QUEUES_URL.format(params.process_id)}",
                headers=self.api_client.auth_header,
                timeout=self.api_client.timeout
            )

            response_payload = GetQueuesResponsePayload(**res.json())
            if res.status_code == 200:
                self.api_client.log_info(response_payload)
            else:
                self.api_client.log_error(response_payload)
            return response_payload

        except BaseException as e:

            self.api_client.log_error(f"Failed to get queues {e}.")

            response_payload = GetQueuesResponsePayload(
                status="error",
                message=str(e)
            )

            return response_payload

    def update_queues(self, params: UpdateQueueRequestPayload) -> APIBaseResponse:

        self.api_client.log_info(f"Updating queue id {params.queue_id}")
        
        try:

            res = requests.put(
                url=f"{self.api_client.ROOT_URL}{self.UPDATE_QUEUE_URL}",
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

            self.api_client.log_error(f"Failed to update queue {e}.")

            response_payload = APIBaseResponse(
                status="error",
                message=str(e)
            )

            return response_payload
