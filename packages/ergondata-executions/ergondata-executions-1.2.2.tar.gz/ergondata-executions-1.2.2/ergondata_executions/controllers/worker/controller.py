import requests
from ergondata_executions.controllers.worker.interfaces import *
from ergondata_executions.controllers.auth.controller import AuthController


class WorkerController:

    CREATE_WORKER_URL = "create/worker"
    DELETE_WORKER_URL = "delete/worker/{0}"
    GET_WORKERS_URL = "get/workers"


    def __init__(self, api_client: AuthController):
        self.api_client = api_client

    def create_worker(self, params: CreateWorkerRequestPayload) -> CreateWorkerResponsePayload:

        self.api_client.log_info(f"Creating worker.")

        try:

            res = requests.post(
                url=f"{self.api_client.ROOT_URL}{self.CREATE_WORKER_URL}",
                json=params.model_dump(),
                headers=self.api_client.auth_header,
                timeout=self.api_client.timeout
            )

            response_payload = CreateWorkerResponsePayload(**res.json())
            if res.status_code == 200:
                self.api_client.log_info(response_payload)
            else:
                self.api_client.log_error(response_payload)
            return response_payload

        except BaseException as e:

            self.api_client.log_error(f"Failed to create worker{e}.")

            response_payload = CreateWorkerResponsePayload(
                status="error",
                message=str(e)
            )

            return response_payload

    def delete_worker(self, params: DeleteWorkerRequestPayload) -> APIBaseResponse:

        self.api_client.log_info(f"Deleting worker id {params.worker_id}")

        try:

            res = requests.delete(
                url=f"{self.api_client.ROOT_URL}{self.DELETE_WORKER_URL.format(params.worker_id)}",
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

            self.api_client.log_error(f"Failed to delete worker{e}.")

            response_payload = CreateWorkerResponsePayload(
                status="error",
                message=str(e)
            )

            return response_payload

    def get_workers(self) -> GetWorkersResponsePayload:

        self.api_client.log_info(f"Getting workers")

        try:

            res = requests.get(
                url=f"{self.api_client.ROOT_URL}{self.GET_WORKERS_URL}",
                headers=self.api_client.auth_header,
                timeout=self.api_client.timeout
            )

            response_payload = GetWorkersResponsePayload(**res.json())
            if res.status_code == 200:
                self.api_client.log_info(response_payload)
            else:
                self.api_client.log_error(response_payload)
            return response_payload

        except BaseException as e:

            self.api_client.log_error(f"Failed to get workers {e}.")

            response_payload = GetWorkersResponsePayload(
                status="error",
                message=str(e)
            )

            return response_payload

