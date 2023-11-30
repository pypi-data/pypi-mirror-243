import datetime

from pydantic import BaseModel, StrictBool, StrictStr, validator
from typing import Optional, List, Literal
from ergondata_executions.interfaces import IEmailRecipient, IEmailIntegrationData, APIBaseResponse


class IQueueProcessingException(BaseModel):
    id: StrictStr
    name: StrictStr
    description: StrictStr
    email_integration: Optional[IEmailIntegrationData]
    created_at: Optional[datetime.datetime]
    updated_at: Optional[datetime.datetime]


class IQueueProcessingExceptions(BaseModel):
    queue_processing_exceptions: List[IQueueProcessingException] = []


class CreateQueueProcessingExceptionRequestPayload(BaseModel):
    queue_id: StrictStr
    queue_processing_exception_name: StrictStr
    queue_processing_exception_description: StrictStr
    queue_processing_exception_type: Literal["system_error", "business_exception"]
    queue_processing_exception_email_integration: StrictBool
    queue_processing_exception_email_recipients: Optional[List[IEmailRecipient]]

    @classmethod
    @validator("queue_processing_exception_email_recipients", pre=True)
    def validate_username_field(cls, value, values):
        if values.get("queue_processing_exception_email_integration"):
            if not value:
                raise ValueError(
                    "If you set email integration to True, then you must provide a list of email recipients."
                )
        return value


class CreateQueueProcessingExceptionResponsePayload(APIBaseResponse):
    queue_processing_exception_id: Optional[StrictStr] = None


class DeleteQueueProcessingExceptionRequestPayload(BaseModel):
    queue_processing_exception_id: StrictStr


class UpdateEmailRecipientsIntegrationPayload(BaseModel):
    action: Literal["overwrite", "add", "remove"]
    emails: List[IEmailRecipient]


class UpdateEmailIntegrationPayload(BaseModel):
    active: Optional[StrictBool]
    recipients: Optional[UpdateEmailRecipientsIntegrationPayload]


class UpdateQueueProcessingExceptionRequestPayload(BaseModel):
    queue_processing_exception_id: StrictStr
    queue_processing_exception_name: Optional[StrictStr]
    queue_processing_exception_description: Optional[StrictStr]
    queue_processing_exception_email_integration: Optional[UpdateEmailIntegrationPayload]


class GetQueueProcessingExceptionsRequestPayload(BaseModel):
    queue_id: StrictStr


class GetQueueProcessingExceptionsResponsePayload(APIBaseResponse):
    data: Optional[IQueueProcessingExceptions] = None

