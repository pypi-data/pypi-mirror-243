import datetime

from pydantic import BaseModel, StrictInt, StrictBool, StrictStr, validator
from typing import Optional, Literal, List, Union
from ergondata_executions.interfaces import APIBaseResponse
from ergondata_executions.controllers.task_processing_exception.interfaces import ITaskProcessingException


class ITaskExecutionProcessingStatus(BaseModel):
    id: Literal["success", "reset", "system_error", "business_exception"]
    title: StrictStr


class ITaskExecution(BaseModel):
    id: StrictStr
    task_execution_status_id: Literal["success", "reset", "system_error", "business_exception", "processing"]
    task_id: StrictStr
    worker_id: StrictStr
    task_exception: Union[Optional[ITaskProcessingException], None] = None
    created_at: Optional[datetime.datetime]
    finished_at: Optional[datetime.datetime]


class ITaskExecutions(BaseModel):
    task_executions: List[ITaskExecution] = []


class CreateTaskExecutionRequestPayload(BaseModel):
    task_id: StrictStr
    dev_mode: StrictBool


class CreateTaskExecutionResponsePayload(APIBaseResponse):
    execution_token: Optional[StrictStr] = None


class UpdateTaskExecutionRequestPayload(BaseModel):
    task_execution_status_id: Optional[Literal["system_error", "business_exception", "success"]] = None
    task_execution_status_message: Optional[StrictStr] = None
    task_execution_exception_id: Optional[StrictStr] = None

    @validator("task_execution_status_id", pre=True)
    def task_execution_status_id_field(cls, value, values):
        if not values.get("task_execution_exception_id"):
            if not value:
                raise ValueError(
                    "When updating an execution you must provide a valid process status or a task exception id."
                )
        return value

    @validator("task_execution_exception_id", pre=True, allow_reuse=True)
    def task_execution_exception_id_field(cls, value, values):
        if not values.get("task_execution_status_id"):
            if not value:
                raise ValueError(
                    "When updating an execution you must provide a valid process status or a task exception id."
                )
        return value


class GetTaskExecutionsRequestPayload(BaseModel):
    task_id: StrictStr
    created_at_lte: Optional[StrictStr] = None
    created_at_lt: Optional[StrictStr] = None
    created_at_gte: Optional[StrictStr] = None
    created_at_gt: Optional[StrictStr] = None
    finished_at_lte: Optional[StrictStr] = None
    finished_at_lt: Optional[StrictStr] = None
    finished_at_gte: Optional[StrictStr] = None
    finished_at_gt: Optional[StrictStr] = None
    processing_status_id: Optional[Literal["success", "system_error", "business_exception"]] = None
    processing_exception_id: Optional[StrictStr] = None
    worker_id: Optional[StrictStr] = None


class GetTaskExecutionsResponsePayload(APIBaseResponse):
    data: Optional[ITaskExecutions] = None
