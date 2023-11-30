import datetime
from pydantic import BaseModel, StrictInt, StrictBool, StrictStr, validator
from typing import Union, Optional, List, Literal
from ergondata_executions.interfaces import APIBaseResponse


class IProcess(BaseModel):
    id: StrictStr
    name: StrictStr
    created_at: datetime.datetime
    updated_at: datetime.datetime


class IProcesses(BaseModel):
    processes: List[IProcess] = []


class GetProcessesErrorResponsePayload(BaseModel):
    error: StrictStr


class GetProcessesResponsePayload(APIBaseResponse):
    data: Optional[IProcesses]


class GetProcessesRequestPayload(BaseModel):
    database_id: StrictStr


class CreateProcessRequestPayload(BaseModel):
    process_title: StrictStr
    process_description: StrictStr
    database_id: StrictStr


class CreateProcessResponsePayload(APIBaseResponse):
    process_id: Optional[StrictStr] = None


class UpdateProcessRequestPayload(BaseModel):
    process_id: StrictStr
    process_name: StrictStr


class DeleteProcessRequestPayload(BaseModel):
    process_id: StrictStr


class CreateProcessMemberRequestPayload(BaseModel):
    process_id: StrictStr
    process_member_email: StrictStr
    process_member_username: Optional[StrictStr]
    process_member_password: Optional[StrictStr]

    @validator("process_member_username", pre=True, always=True, allow_reuse=True)
    def validate_username_field(cls, value, values):
        if values.get("process_member_password"):
            if not value:
                raise ValueError(
                    "If you want to create a new user as a db member please send username and password keys."
                )
        return value

    @validator("process_member_password", pre=True, always=True)
    def validate_password_field(cls, value, values):
        if values.get("process_member_username"):
            if not value:
                raise ValueError(
                    "If you want to create a new user as a db member please send username and password keys."
                )
        return value


class CreateProcessMemberResponsePayload(APIBaseResponse):
    process_member_id: Optional[StrictStr] = None


class GetProcessMembersRequestPayload(BaseModel):
    process_id: StrictStr


class IUser(BaseModel):
    id: StrictStr
    username: StrictStr
    email: Optional[StrictStr]


class IProcessMember(BaseModel):
    id: StrictStr
    email: StrictStr
    created_at: datetime.datetime
    updated_at: datetime.datetime


class IProcessMembers(BaseModel):
    process_members: List[IProcessMember] = []


class GetProcessMembersResponsePayload(APIBaseResponse):
    data: Optional[IProcessMembers] = None


class DeleteProcessMemberRequestPayload(BaseModel):
    process_member_id: StrictStr


class AddProcessMemberPermissionsRequestPayload(BaseModel):
    process_member_id: StrictStr
    process_member_permissions: List[StrictStr]


class DeleteProcessMemberPermissionsRequestPayload(BaseModel):
    process_member_id: StrictStr
    process_member_permission_id: StrictStr


class IUserPermission(BaseModel):
    id: StrictStr
    name: StrictStr
    type: Literal["db_member", "client_owner", "process_member"]
    created_at: datetime.datetime
    updated_at: datetime.datetime


class IUserPermissions(BaseModel):
    user_permissions: List[IUserPermission] = []


class GetProcessMemberPermissionsResponsePayload(APIBaseResponse):
    data: IUserPermissions


class GetProcessMemberPermissionsRequestPayload(BaseModel):
    process_member_id: StrictStr

