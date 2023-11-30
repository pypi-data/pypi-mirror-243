import datetime
from pydantic import BaseModel, StrictInt, StrictBool, StrictStr, validator
from typing import Union, Optional, List, Literal
from ergondata_executions.interfaces import APIBaseResponse


class IDatabase(BaseModel):
    id: StrictStr
    name: StrictStr
    created_at: datetime.datetime
    updated_at: datetime.datetime


class IDatabases(BaseModel):
    databases: List[IDatabase] = []


class GetDatabasesErrorResponsePayload(BaseModel):
    error: StrictStr


class GetDatabasesResponsePayload(APIBaseResponse):
    data: Optional[IDatabases]


class CreateDatabaseRequestPayload(BaseModel):
    database_name: StrictStr


class CreateDatabaseResponsePayload(APIBaseResponse):
    database_id: Optional[StrictStr] = None


class UpdateDatabaseRequestPayload(BaseModel):
    database_id: StrictStr
    database_name: StrictStr


class DeleteDatabaseRequestPayload(BaseModel):
    database_id: StrictStr


class CreateDatabaseMemberRequestPayload(BaseModel):
    database_id: StrictStr
    database_member_email: StrictStr
    database_member_username: Optional[StrictStr] = None


class CreateDatabaseMemberResponsePayload(APIBaseResponse):
    database_member_id: Optional[StrictStr] = None


class GetDatabaseMembersRequestPayload(BaseModel):
    database_id: StrictStr


class IUser(BaseModel):
    id: StrictStr
    email: Optional[StrictStr] = None
    first_name: Optional[StrictStr] = None


class IDatabaseMember(BaseModel):
    id: StrictStr
    user: IUser
    created_at: datetime.datetime
    updated_at: datetime.datetime


class IDatabaseMembers(BaseModel):
    database_members: List[IDatabaseMember] = []


class GetDatabaseMembersResponsePayload(APIBaseResponse):
    data: Optional[IDatabaseMembers] = None


class DeleteDatabaseMemberRequestPayload(BaseModel):
    database_member_id: StrictStr


class AddDatabaseMemberPermissionsRequestPayload(BaseModel):
    database_member_id: StrictStr
    database_member_permissions: List[StrictStr]


class DeleteDatabaseMemberPermissionsRequestPayload(BaseModel):
    database_member_id: StrictStr
    database_member_permission_id: StrictStr


class IUserPermission(BaseModel):
    id: StrictStr
    name: StrictStr
    type: Literal["db_member", "client_owner", "process_member"]
    created_at: datetime.datetime
    updated_at: datetime.datetime


class IUserPermissions(BaseModel):
    user_permissions: List[IUserPermission] = []


class GetDatabaseMemberPermissionsResponsePayload(APIBaseResponse):
    data: IUserPermissions


class GetDatabaseMemberPermissionsRequestPayload(BaseModel):
    database_member_id: StrictStr

