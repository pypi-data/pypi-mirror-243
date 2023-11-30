import datetime

from pydantic import BaseModel, StrictInt, StrictBool, StrictStr
from typing import Optional, List, Literal
from ergondata_executions.interfaces import APIBaseResponse
from ergondata_executions.controllers.task_execution.interfaces import ITaskExecution



class CreateTaskExecutionLogRequestPayload(BaseModel):
    log_type: Literal["info", "warning", "error"]
    log_message: Optional[StrictStr]
    log_task_step_id: Optional[StrictStr] = None


class ITaskExecutionLog(BaseModel):
    log_id: StrictStr
    log_type: StrictStr
    log_message: StrictStr
    log_task_execution_id: StrictStr
    log_task_execution_worker_id: StrictStr
    log_task_execution_worker_username: StrictStr
    log_created_at: datetime.datetime
    task_step_id: Optional[StrictStr] = None


class GetTaskExecutionLogsRequestPayload(BaseModel):
    task_id: StrictStr
    task_execution_id: Optional[StrictStr] = None
    log_type: Optional[Literal["info", "waring", "error"]] = None
    created_at_lte: Optional[StrictStr] = None
    created_at_lt: Optional[StrictStr] = None
    created_at_gte: Optional[StrictStr] = None
    created_at_gt: Optional[StrictStr] = None


class ITaskExecutionLogs(BaseModel):
    task_execution_logs: List[ITaskExecutionLog] = None


class GetTaskExecutionLogsResponsePayload(APIBaseResponse):
    data: Optional[ITaskExecutionLogs] = None

