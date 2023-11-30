from pydantic import BaseModel, StrictStr
from typing import Union, Optional
from ergondata_executions.interfaces import APIBaseResponse


class AuthRequestPayload(BaseModel):
    username: StrictStr
    password: StrictStr
    client_id: StrictStr


class AuthSuccessResponsePayload(BaseModel):
    token: Optional[Union[StrictStr, None]]


class AuthResponsePayload(APIBaseResponse):
    token: Optional[StrictStr] = None

