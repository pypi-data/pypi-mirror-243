import datetime

from pydantic import BaseModel, StrictBool, StrictStr, validator
from typing import Optional, List, Literal, Union
from ergondata_executions.interfaces import IEmailRecipient, UpdateEmailRecipientsPayload, IEmailIntegrationData, APIBaseResponse



class ITaskProcessingException(BaseModel):
    id: StrictStr
    name: StrictStr
    description: StrictStr
    email_integration: Optional[IEmailIntegrationData]
    created_at: Optional[datetime.datetime]
    updated_at: Optional[datetime.datetime]


class ITaskProcessingExceptions(BaseModel):
    task_processing_exceptions: List[ITaskProcessingException] = []


class CreateTaskProcessingExceptionRequestPayload(BaseModel):
    task_id: StrictStr
    task_processing_exception_name: StrictStr
    task_processing_exception_description: StrictStr
    task_processing_exception_status_id: Literal["business_exception", "system_error"]
    task_processing_exception_email_integration: StrictBool
    task_processing_exception_email_recipients: Optional[List[IEmailRecipient]]

    @classmethod
    @validator("task_processing_exception_email_recipients", pre=True)
    def validate_username_field(cls, value, values):
        if values.get("task_processing_exception_email_integration"):
            if not value:
                raise ValueError(
                    "If you set email integration to True, then you must provide a list of email recipients."
                )
        return value


class CreateTaskProcessingExceptionResponsePayload(APIBaseResponse):
    task_processing_exception_id: StrictStr


class DeleteTaskProcessingExceptionRequestPayload(BaseModel):
    task_processing_exception_id: StrictStr


class UpdateEmailRecipientsIntegrationPayload(BaseModel):
    action: Literal["overwrite", "add", "remove"]
    emails: List[IEmailRecipient]


class UpdateEmailIntegrationPayload(BaseModel):
    active: StrictBool
    recipients: Optional[UpdateEmailRecipientsIntegrationPayload]


class UpdateTaskProcessingExceptionRequestPayload(BaseModel):
    task_processing_exception_id: StrictStr
    task_processing_exception_name: Optional[StrictStr]
    task_processing_exception_description: Optional[StrictStr]
    task_processing_exception_email_integration: Optional[UpdateEmailIntegrationPayload]


class GetTaskProcessingExceptionsRequestPayload(BaseModel):
    task_id: StrictStr


class GetTaskProcessingExceptionsResponsePayload(APIBaseResponse):
    data: Optional[ITaskProcessingExceptions] = None

