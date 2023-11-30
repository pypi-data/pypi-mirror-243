import datetime

from pydantic import BaseModel, StrictBool, StrictStr, validator
from typing import Optional, List
from typing_extensions import Literal
from ergondata_executions.interfaces import IEmailRecipient, IEmailIntegrationData, APIBaseResponse


class ITaskEmailIntegration(BaseModel):
    task_started: IEmailIntegrationData
    task_succeeded: IEmailIntegrationData
    task_failed: IEmailIntegrationData


class ITask(BaseModel):
    id: StrictStr
    name: StrictStr
    description: Optional[StrictStr]
    email_integration: Optional[ITaskEmailIntegration]
    created_at: Optional[datetime.datetime]
    updated_at: Optional[datetime.datetime]


class ITasks(BaseModel):
    tasks: List[ITask] = []


class CreateTaskResponsePayload(APIBaseResponse):
    task_id: Optional[StrictStr] = None


class CreateTaskRequestPayload(BaseModel):
    task_name: StrictStr
    task_description: StrictStr
    process_id: StrictStr
    task_type: Literal["dispatcher", "performer", "performer-and-dispatcher"]
    task_succeeded_email_integration: StrictBool
    task_succeeded_email_recipients: Optional[List[IEmailRecipient]]
    task_failed_email_integration: StrictBool
    task_failed_email_recipients: Optional[List[IEmailRecipient]]
    task_started_email_integration: StrictBool
    task_started_email_recipients: Optional[List[IEmailRecipient]]
    queue_id: Optional[StrictStr] = None

    @validator("task_succeeded_email_recipients", pre=True, always=True, allow_reuse=True)
    def validate_succeeded_email_recipients(cls, value, values):
        if values.get("task_succeeded_email_integration"):
            if not value:
                raise ValueError(
                    "task_succeeded_email_recipients must be provided when task_succeeded_email_integration is True")
        return value

    @validator("task_started_email_recipients", pre=True, always=True, allow_reuse=True)
    def validate_started_email_recipients(cls, value, values):
        if values.get("task_started_email_integration"):
            if not value:
                raise ValueError(
                    "task_started_email_recipients must be provided when task_started_email_integration is True")
        return value

    @validator("task_failed_email_recipients", pre=True, always=True, allow_reuse=True)
    def validate_failed_email_recipients(cls, value, values):
        if values.get("task_failed_email_integration"):
            if not value:
                raise ValueError(
                    "task_failed_email_recipients must be provided when task_failed_email_integration is True")
        return value


class DeleteTaskRequestPayload(BaseModel):
    task_id: StrictStr


class GetTasksRequestPayload(BaseModel):
    process_id: StrictStr


class GetTasksResponsePayload(APIBaseResponse):
    data: Optional[ITasks] = None


class UpdateTaskEmailRecipientsPayload(BaseModel):
    action: Literal["overwrite", "add", "remove"]
    emails: List[IEmailRecipient]


class UpdateTaskEmailIntegrationPayload(BaseModel):
    active: Optional[StrictBool] = None
    recipients: Optional[UpdateTaskEmailRecipientsPayload]


class UpdateTaskEmailIntegration(BaseModel):
    task_started: Optional[UpdateTaskEmailIntegrationPayload]
    task_succeeded: Optional[UpdateTaskEmailIntegrationPayload]
    task_failed: Optional[UpdateTaskEmailIntegrationPayload]


class UpdateTaskRequestPayload(BaseModel):
    task_id: StrictStr
    task_name: Optional[StrictStr]
    task_description: Optional[StrictStr]
    task_email_integration: Optional[UpdateTaskEmailIntegration]



