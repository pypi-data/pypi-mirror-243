import requests
from ergondata_executions.controllers.database.interfaces import *
from ergondata_executions.controllers.auth.controller import AuthController
from ergondata_executions.controllers.process.controller import ProcessController


class DBMemberController(ProcessController):

    CREATE_DB_MEMBER_URL = "create/database/member"
    GET_DB_MEMBERS_URL = "get/database/{0}/members"
    DELETE_DB_MEMBER_URL = "delete/database/member/{0}"
    ADD_DB_MEMBER_PERMISSIONS_URL = "create/database/member/permissions"
    DELETE_DB_MEMBER_PERMISSIONS_URL = "delete/database/member/{0}/permission/{1}"
    GET_DB_MEMBER_PERMISSIONS_URL = "get/database/member/{0}/permissions"

    def __init__(self, api_client: AuthController):
        self.api_client = api_client
        super(DBMemberController, self).__init__(api_client=api_client)

    def create_database_member(
        self,
        params: CreateDatabaseMemberRequestPayload
    ) -> CreateDatabaseMemberResponsePayload:

        self.api_client.log_info(f"Adding database member to database {params.database_id}.")

        try:

            res = requests.post(
                url=f"{self.api_client.ROOT_URL}{self.CREATE_DB_MEMBER_URL}",
                json=params.model_dump(),
                headers=self.api_client.auth_header,
                timeout=self.api_client.timeout
            )

            response_payload = CreateDatabaseMemberResponsePayload(**res.json())
            if res.status_code == 200:
                self.api_client.log_info(response_payload)
            else:
                self.api_client.log_error(response_payload)
                
            return response_payload

        except BaseException as e:
            self.api_client.log_error(f"Failed to create database member {e}")
            response_payload = CreateDatabaseMemberResponsePayload(
                status="error",
                message=str(e)
            )

            return response_payload

    def get_database_members(self, params: GetDatabaseMembersRequestPayload) -> GetDatabaseMembersResponsePayload:

        self.api_client.log_info(f"Getting database members for database {params.database_id}.")

        try:

            res = requests.get(
                url=f"{self.api_client.ROOT_URL}{self.GET_DB_MEMBERS_URL.format(params.database_id)}",
                json=params.model_dump(),
                headers=self.api_client.auth_header,
                timeout=self.api_client.timeout
            )

            response_payload = GetDatabaseMembersResponsePayload(**res.json())

            if res.status_code == 200:
                self.api_client.log_info(response_payload)
            else:
                self.api_client.log_error(response_payload)

            return response_payload

        except BaseException as e:
            self.api_client.log_error(f"Failed to delete database {e}.")
            response_payload = GetDatabaseMembersResponsePayload(
                status="error",
                message=str(e)
            )

            return response_payload

    def delete_database_member(self, params: DeleteDatabaseMemberRequestPayload) -> APIBaseResponse:

        self.api_client.log_info(f"Deleting database member id {params.database_member_id}.")

        try:

            res = requests.delete(
                url=f"{self.api_client.ROOT_URL}{self.DELETE_DB_MEMBER_URL.format(params.database_member_id)}",
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

            self.api_client.log_error(f"Failed to delete database member {e}.")
            response_payload = APIBaseResponse(
                status="error",
                message=str(e)
            )

            return response_payload

    def add_database_member_permissions(self, params: AddDatabaseMemberPermissionsRequestPayload) -> APIBaseResponse:

        self.api_client.log_info(
            f"Adding database member id {params.database_member_id} permissions {params.database_member_permissions}."
        )

        try:

            res = requests.post(
                url=f"{self.api_client.ROOT_URL}{DBMemberController.ADD_DB_MEMBER_PERMISSIONS_URL}",
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

            self.api_client.log_error(f"Failed to add database member permissions {e}.")

            response_payload = APIBaseResponse(
                status="error",
                message=str(e)
            )

            return response_payload

    def remove_database_member_permissions(self, params: DeleteDatabaseMemberPermissionsRequestPayload) -> APIBaseResponse:

        """
            This method is used to delete database member permissions
        """


        self.api_client.log_info(f"Deleting database member id {params.database_member_id} permission {params.database_member_permission_id}.")

        try:

            res = requests.delete(
                url=f"{self.api_client.ROOT_URL}{self.DELETE_DB_MEMBER_PERMISSIONS_URL.format(params.database_member_id, params.database_member_permission_id)}",
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

            self.api_client.log_error(f"Failed to delete database member permissions {e}.")

            response_payload = APIBaseResponse(
                status="error",
                message=str(e)
            )

            return response_payload

    def get_database_member_permissions(self, params: GetDatabaseMemberPermissionsRequestPayload) -> GetDatabaseMemberPermissionsResponsePayload:

        """
            This method is used to get a database member permissions
        """

        self.api_client.log_info(f"Getting database member {params.database_member_id} permissions.")

        try:

            res = requests.get(
                url=f"{self.api_client.ROOT_URL}{self.GET_DB_MEMBER_PERMISSIONS_URL.format(params.database_member_id)}",
                json=params.model_dump(),
                headers=self.api_client.auth_header,
                timeout=self.api_client.timeout
            )

            response_payload = GetDatabaseMemberPermissionsResponsePayload(**res.json())
            if res.status_code == 200:
                self.api_client.log_info(response_payload)
            else:
                self.api_client.log_error(response_payload)

            return response_payload

        except BaseException as e:

            self.api_client.log_error(f"Failed to delete get databases member permissions {e}.")

            response_payload = GetDatabaseMemberPermissionsResponsePayload(
                status="error",
                message=str(e)
            )

            return response_payload


class DBController(DBMemberController):

    GET_DBS_URL = "get/databases"
    CREATE_DB_URL = "create/database"
    UPDATE_DB_URL = "update/database"
    DELETE_DB_URL = "delete/database/{0}"

    def __init__(self, api_client: AuthController):
        self.api_client = api_client
        super(DBController, self).__init__(api_client=api_client)

    def get_databases(self) -> GetDatabasesResponsePayload:

        self.api_client.log_info("Getting databases.")

        try:

            res = requests.get(
                url=f"{self.api_client.ROOT_URL}{self.GET_DBS_URL}",
                headers=self.api_client.auth_header,
                timeout=self.api_client.timeout
            )

            response_payload = GetDatabasesResponsePayload(**res.json())
            if res.status_code == 200:
                self.api_client.log_info(response_payload)
            else:
                self.api_client.log_error(response_payload)

            return response_payload

        except BaseException as e:

            self.api_client.log_error(f"Failed to get databases {e}.")
            response_payload = GetDatabasesResponsePayload(
                status="error",
                message=str(e)
            )
            return response_payload

    def create_database(self, params: CreateDatabaseRequestPayload) -> CreateDatabaseResponsePayload:

        """
            This method is used to create a database
        """

        self.api_client.log_info(message=f"Creating database {params.database_name}.")

        try:

            res = requests.post(
                url=f"{self.api_client.ROOT_URL}{self.CREATE_DB_URL}",
                json=params.model_dump(),
                headers=self.api_client.auth_header,
                timeout=self.api_client.timeout
            )
            response_payload = CreateDatabaseResponsePayload(**res.json())
            if res.status_code == 200:
                self.api_client.log_info(response_payload)
            else:
                self.api_client.log_error(response_payload)

            return response_payload

        except BaseException as e:

            self.api_client.log_error(f"Failed to create database {e}.")
            response_payload = CreateDatabaseResponsePayload(
                status="error",
                message=str(e)
            )
            return response_payload

    def update_database(self, params: UpdateDatabaseRequestPayload) -> APIBaseResponse:

        """
            This method is used to update a database name
        """

        self.api_client.log_info(f"Updating database {params.database_id}.")
        try:

            res = requests.put(
                url=f"{self.api_client.ROOT_URL}{self.UPDATE_DB_URL}",
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

            self.api_client.log_error(f"Failed to update database {e}.")
            response_payload = APIBaseResponse(
                status="error",
                message=str(e)
            )
            return response_payload

    def delete_database(self, params: DeleteDatabaseRequestPayload) -> APIBaseResponse:


        self.api_client.log_info(f"Deleting database {params.database_id}.")

        try:

            res = requests.delete(
                url=f"{self.api_client.ROOT_URL}{self.DELETE_DB_URL.format(params.database_id)}",
                headers=self.api_client.auth_header,
                timeout=self.api_client.timeout
            )

            response_payload = APIBaseResponse(**res.json())
            response_payload = APIBaseResponse(**res.json())
            if res.status_code == 200:
                self.api_client.log_info(response_payload)
            else:
                self.api_client.log_error(response_payload)

            return response_payload
        except BaseException as e:

            self.api_client.log_error(f"Failed to delete database {e}.")

            response_payload = CreateDatabaseResponsePayload(
                status="error",
                message=str(e)
            )
            return response_payload


