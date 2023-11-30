import requests
from ergondata_executions.controllers.task_execution_log.interfaces import *
from ergondata_executions.controllers.auth.controller import AuthController


class TaskExecutionLogController:

    CREATE_TASK_EXECUTION_LOG_URL = "create/database/process/task/execution/log"
    GET_TASK_EXECUTION_LOGS_URL = "get/database/process/task/{0}/execution/logs?"

    def __init__(self, api_client: AuthController):
        self.api_client = api_client

    def create_task_execution_log(
        self,
        params: CreateTaskExecutionLogRequestPayload
    ) -> APIBaseResponse:

        if params.log_type == "info":
            self.api_client.log_info(params.log_message)
        else:
            self.api_client.log_error(params.log_message)

        try:

            res = requests.post(
                url=f"{self.api_client.ROOT_URL}{self.CREATE_TASK_EXECUTION_LOG_URL}",
                json=params.model_dump(),
                headers=self.api_client.exec_header,
                timeout=self.api_client.timeout
            )

            response_payload = APIBaseResponse(**res.json())

            if res.status_code == 200:
                pass
            else:
                self.api_client.log_error(response_payload)
            return response_payload

        except BaseException as e:

            self.api_client.log_error(f"Failed to create task_execution log {e}.")

            response_payload = APIBaseResponse(
                status="error",
                message=str(e)
            )

            return response_payload

    def get_task_execution_logs(
        self,
        params: GetTaskExecutionLogsRequestPayload
    ):


        self.api_client.log_info(f"Getting task execution logs for task {params.task_id}")

        try:

            get_task_url = self.GET_TASK_EXECUTION_LOGS_URL.format(params.task_id)

            get_task_url = get_task_url + f'created_at_lt={params.created_at_lt}&' if params.created_at_lt else get_task_url
            get_task_url = get_task_url + f'created_at_lte={params.created_at_lte}&' if params.created_at_lte else get_task_url
            get_task_url = get_task_url + f'created_at_gt={params.created_at_gt}&' if params.created_at_gt else get_task_url
            get_task_url = get_task_url + f'created_at_gte={params.created_at_gte}&' if params.created_at_gte else get_task_url
            get_task_url = get_task_url + f'log_type={params.log_type}&' if params.log_type else get_task_url
            get_task_url = get_task_url + f'task_execution_id={params.task_execution_id}&' if params.task_execution_id else get_task_url

            res = requests.get(
                url=f"{self.api_client.ROOT_URL}{get_task_url}",
                headers=self.api_client.auth_header,
                timeout=self.api_client.timeout
            )
            response_payload = GetTaskExecutionLogsResponsePayload(**res.json())

            if res.status_code == 200:
                self.api_client.log_info(response_payload)
            else:
                self.api_client.log_error(response_payload)
            return response_payload

        except BaseException as e:

            self.api_client.log_error(f"Failed to get task execution logs {e}.")

            response_payload = GetTaskExecutionLogsResponsePayload(
                status="error",
                message=str(e)
            )

            return response_payload
