import datetime
from pydantic import BaseModel, StrictInt, StrictBool, StrictStr
from typing import Optional, List
from ergondata_executions.interfaces import APIBaseResponse
from ergondata_executions.controllers.database.interfaces import IUser


class IWorker(BaseModel):
    id: StrictStr
    user: IUser
    created_at: datetime.datetime
    updated_at: datetime.datetime


class IWorkers(BaseModel):
    workers: List[IWorker] = []


class CreateWorkerRequestPayload(BaseModel):
    worker_first_name: StrictStr


class CreateWorkerResponsePayload(APIBaseResponse):
    worker_id: Optional[StrictStr] = None


class DeleteWorkerRequestPayload(BaseModel):
    worker_id: StrictStr


class GetWorkersResponsePayload(APIBaseResponse):
    data: IWorkers




