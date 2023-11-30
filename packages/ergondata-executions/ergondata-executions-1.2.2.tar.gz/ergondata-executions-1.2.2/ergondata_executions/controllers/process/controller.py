import requests
from ergondata_executions.controllers.process.interfaces import *
from ergondata_executions.controllers.auth.controller import AuthController


class ProcessMemberController:

    CREATE_PROCESS_MEMBER_URL = "create/database/process/member"
    GET_PROCESS_MEMBERS_URL = "get/database/process/{0}/members"
    DELETE_PROCESS_MEMBER_URL = "delete/database/process/member/{0}"
    ADD_PROCESS_MEMBER_PERMISSIONS_URL = "create/database/process/member/permissions"
    DELETE_PROCESS_MEMBER_PERMISSIONS_URL = "delete/database/process/member/{0}/permission/{1}"
    GET_PROCESS_MEMBER_PERMISSIONS_URL = ""

    def __init__(self, api_client: AuthController):
        self.api_client = api_client

    def create_process_member(self, params: CreateProcessMemberRequestPayload) -> CreateProcessMemberResponsePayload:

        self.api_client.log_info(f"Adding Process member to process {params.process_id}.")

        try:

            res = requests.post(
                url=f"{self.api_client.ROOT_URL}{self.CREATE_PROCESS_MEMBER_URL}",
                json=params.model_dump(),
                headers=self.api_client.auth_header,
                timeout=self.api_client.timeout
            )

            response_payload = CreateProcessMemberResponsePayload(**res.json())
            
            if res.status_code == 200:
                self.api_client.log_info(response_payload)
            else:
                self.api_client.log_error(response_payload)
            return response_payload

        except BaseException as e:

            self.api_client.log_error(f"Failed to add process member {e}.")

            response_payload = CreateProcessMemberResponsePayload(
                status="error",
                message=str(e)
            )

            return response_payload

    def get_process_members(self, params: GetProcessMembersRequestPayload) -> GetProcessMembersResponsePayload:

        self.api_client.log_info(f"Getting process members for Process {params.process_id}.")

        try:

            res = requests.get(
                url=f"{self.api_client.ROOT_URL}{self.GET_PROCESS_MEMBERS_URL.format(params.process_id)}",
                json=params.model_dump(),
                headers=self.api_client.auth_header,
                timeout=self.api_client.timeout
            )

            response_payload = GetProcessMembersResponsePayload(**res.json())
            if res.status_code == 200:
                self.api_client.log_info(response_payload)
            else:
                self.api_client.log_error(response_payload)
            return response_payload

        except BaseException as e:

            self.api_client.log_error(f"Failed to get process members {e}.")
            response_payload = GetProcessMembersResponsePayload(
                status="error",
                message=str(e)
            )

            return response_payload

    def delete_process_member(self, params: DeleteProcessMemberRequestPayload) -> APIBaseResponse:

        self.api_client.log_info(f"Deleting Process member id {params.process_member_id}.")

        try:

            res = requests.delete(
                url=f"{self.api_client.ROOT_URL}{self.DELETE_PROCESS_MEMBER_URL.format(params.process_member_id)}",
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

            self.api_client.log_error(f"Failed to delete process member {e}.")

            response_payload = APIBaseResponse(
                status="error",
                message=str(e)
            )

            return response_payload

    def add_process_member_permissions(self, params: AddProcessMemberPermissionsRequestPayload) -> APIBaseResponse:

        self.api_client.log_info(f"Adding process member id {params.process_member_id} permissions {params.process_member_permissions}.")

        try:

            res = requests.post(
                url=f"{self.api_client.ROOT_URL}{ProcessMemberController.ADD_PROCESS_MEMBER_PERMISSIONS_URL}",
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

            self.api_client.log_error(f"Failed to add Process member permissions {e}.")

            response_payload = APIBaseResponse(
                status="error",
                message=str(e)
            )

            return response_payload

    def remove_process_member_permissions(self, params: DeleteProcessMemberPermissionsRequestPayload) -> APIBaseResponse:

        self.api_client.log_info(f"Deleting Process member id {params.process_member_id} permission {params.process_member_permission_id}.")

        try:

            res = requests.delete(
                url=f"{self.api_client.ROOT_URL}{self.DELETE_PROCESS_MEMBER_PERMISSIONS_URL.format(params.process_member_id, params.process_member_permission_id)}",
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

            self.api_client.log_error(f"Failed to delete Process member permissions {e}.")

            response_payload = APIBaseResponse(
                status="error",
                message=str(e)
            )

            return response_payload

    def get_process_member_permissions(self, params: GetProcessMemberPermissionsRequestPayload) -> GetProcessMemberPermissionsResponsePayload:

        self.api_client.log_info(f"Getting Process member {params.process_member_id} permissions.")

        try:

            res = requests.get(
                url=f"{self.api_client.ROOT_URL}{self.GET_PROCESS_MEMBER_PERMISSIONS_URL.format(params.process_member_id)}",
                json=params.model_dump(),
                headers=self.api_client.auth_header,
                timeout=self.api_client.timeout
            )

            response_payload = GetProcessMemberPermissionsResponsePayload(**res.json())
            if res.status_code == 200:
                self.api_client.log_info(response_payload)
            else:
                self.api_client.log_error(response_payload)
            return response_payload

        except BaseException as e:

            self.api_client.log_error(f"Failed to delete get Process member permissions {e}.")

            response_payload = GetProcessMemberPermissionsResponsePayload(
                status="error",
                message=str(e)
            )

            return response_payload


class ProcessController(ProcessMemberController):

    GET_PROCESSES_URL = "get/database/{0}/processes"
    CREATE_PROCESS_URL = "create/database/process"
    UPDATE_PROCESS_URL = "update/database/process"
    DELETE_PROCESS_URL = "delete/database/process/{0}"

    def __init__(self, api_client: AuthController):
        self.api_client = api_client
        super(ProcessController, self).__init__(api_client=api_client)

    def get_processes(self, params: GetProcessesRequestPayload) -> GetProcessesResponsePayload:

        self.api_client.log_info(f"Getting Processes for database id {params.database_id}.")

        try:

            res = requests.get(
                url=f"{self.api_client.ROOT_URL}{ProcessController.GET_PROCESSES_URL.format(params.database_id)}",
                headers=self.api_client.auth_header,
                timeout=self.api_client.timeout
            )

            response_payload = GetProcessesResponsePayload(**res.json())
            if res.status_code == 200:
                self.api_client.log_info(response_payload)
            else:
                self.api_client.log_error(response_payload)
            return response_payload

        except BaseException as e:

            self.api_client.log_error(f"Failed to get Processes {e}.")

            response_payload = GetProcessesResponsePayload(
                status="error",
                message=str(e)
            )
            return response_payload

    def create_process(self, params: CreateProcessRequestPayload) -> CreateProcessResponsePayload:

        self.api_client.log_info(f"Creating Process {params.process_title}.")

        try:

            res = requests.post(
                url=f"{self.api_client.ROOT_URL}{self.CREATE_PROCESS_URL}",
                json=params.model_dump(),
                headers=self.api_client.auth_header,
                timeout=self.api_client.timeout
            )

            response_payload = CreateProcessResponsePayload(**res.json())
            if res.status_code == 200:
                self.api_client.log_info(response_payload)
            else:
                self.api_client.log_error(response_payload)
            return response_payload

        except BaseException as e:

            self.api_client.log_error(f"Failed to create Process {e}.")

            response_payload = CreateProcessResponsePayload(
                status="error",
                message=str(e)
            )
            return response_payload

    def update_process(self, params: UpdateProcessRequestPayload) -> APIBaseResponse:

        self.api_client.log_info(f"Updating Process {params.process_id}.")

        try:

            res = requests.put(
                url=f"{self.api_client.ROOT_URL}{self.UPDATE_PROCESS_URL}",
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

            self.api_client.log_error(f"Failed to update Process {e}.")

            response_payload = CreateProcessResponsePayload(
                status="error",
                message=str(e)
            )
            return response_payload

    def delete_process(self, params: DeleteProcessRequestPayload) -> APIBaseResponse:

        self.api_client.log_info(f"Deleting Process {params.process_id}.")

        try:

            res = requests.delete(
                url=f"{self.api_client.ROOT_URL}{self.DELETE_PROCESS_URL.format(params.process_id)}",
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

            self.api_client.log_error(f"Failed to delete Process {e}.")

            response_payload = CreateProcessResponsePayload(
                status="error",
                message=str(e)
            )
            return response_payload


