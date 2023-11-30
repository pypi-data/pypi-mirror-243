import datetime

from pydantic import BaseModel, StrictInt, StrictBool, StrictStr, validator
from typing import Optional, List, Union, Any
from typing_extensions import Literal
from ergondata_executions.interfaces import APIBaseResponse, IEmailRecipient, IEmailIntegrationData


class IQueueEmailIntegration(BaseModel):
    queue_item_created: IEmailIntegrationData
    queue_item_started: IEmailIntegrationData
    queue_item_succeeded: IEmailIntegrationData
    queue_item_failed: IEmailIntegrationData


class IQueue(BaseModel):
    id: StrictStr
    name: StrictStr
    description: StrictStr
    allow_to_include_repeated_queue_item: StrictBool
    queue_item_max_retries_within_execution: StrictInt
    queue_item_max_retries_outside_execution: StrictInt
    email_integration: Optional[IQueueEmailIntegration]
    created_at: datetime.datetime
    updated_at: datetime.datetime


class IQueues(BaseModel):
    queues: List[IQueue] = []



class IQueueProcessingException(BaseModel):
    id: StrictStr
    name: StrictStr
    description: StrictStr
    email_integration: Optional[IEmailIntegrationData]
    created_at: Optional[datetime.datetime]
    updated_at: Optional[datetime.datetime]


class IQueueItem(BaseModel):
    id: StrictStr
    payload: Any
    external_id: Optional[StrictStr] = None
    processing_status_id: Optional[StrictStr] = None
    processing_status_message: Optional[StrictStr] = None
    processing_exception_id: Optional[StrictStr] = None
    processing_exception_name: Optional[StrictStr] = None
    max_retries_within: Optional[StrictInt] = None
    max_retries_outside: Optional[StrictInt] = None
    created_at: Optional[datetime.datetime] = None
    started_at: Optional[datetime.datetime] = None
    finished_at: Optional[datetime.datetime] = None


class IQueueItems(BaseModel):
    queue_items: List[IQueueItem] = []


class CreateQueueRequestPayload(BaseModel):
    queue_name: StrictStr
    queue_description: StrictStr
    allow_to_include_repeated_queue_item: Optional[StrictBool]
    queue_item_max_retries_within_execution: Optional[StrictInt]
    queue_item_max_retries_outside_execution: Optional[StrictInt]
    queue_item_created_email_integration: StrictBool
    queue_item_created_email_recipients: Union[List[IEmailRecipient], None]
    queue_item_succeeded_email_integration: StrictBool
    queue_item_succeeded_email_recipients: Union[List[IEmailRecipient], None]
    queue_item_failed_email_integration: StrictBool
    queue_item_failed_email_recipients: Union[List[IEmailRecipient], None]
    queue_item_started_email_integration: StrictBool
    queue_item_started_email_recipients: Union[List[IEmailRecipient], None]
    process_id: StrictStr


class CreateQueueResponsePayload(APIBaseResponse):
    queue_id: StrictStr


class DeleteQueueRequestPayload(BaseModel):
    queue_id: StrictStr


class GetQueuesRequestPayload(BaseModel):
    process_id: StrictStr


class GetQueuesResponsePayload(APIBaseResponse):
    data: IQueues



class UpdateQueueEmailRecipientsPayload(BaseModel):
    action: Literal["overwrite", "add", "remove"]
    emails: List[IEmailRecipient]


class UpdateQueueEmailIntegrationPayload(BaseModel):
    active: Optional[StrictBool] = None
    recipients: Optional[UpdateQueueEmailRecipientsPayload]


class UpdateQueueEmailIntegration(BaseModel):
    queue_item_created: Optional[UpdateQueueEmailIntegrationPayload]
    queue_item_started: Optional[UpdateQueueEmailIntegrationPayload]
    queue_item_succeeded: Optional[UpdateQueueEmailIntegrationPayload]
    queue_item_failed: Optional[UpdateQueueEmailIntegrationPayload]


class UpdateQueueRequestPayload(BaseModel):
    queue_id: StrictStr
    queue_name: Optional[StrictStr]
    queue_description: Optional[StrictStr]
    email_integration: Optional[UpdateQueueEmailIntegration]
    allow_to_include_repeated_queue_item: Optional[StrictBool]
    queue_item_max_retries_within_execution: Optional[StrictInt]
    queue_item_max_retries_outside_execution: Optional[StrictInt]


class CreateQueueItemRequestPayload(BaseModel):
    queue_id: StrictStr
    payload: object
    external_id: Optional[StrictStr] = None
    processing_status_message: Optional[StrictStr] = None
    processing_status_id: Optional[Literal["business_exception", "system_error", "success", "pending"]] = "pending"
    processing_exception_id: Optional[StrictStr] = None


class CreateQueueItemResponsePayload(APIBaseResponse):
    queue_item_id: Optional[StrictStr] = None


class GetQueueItemRequestPayload(BaseModel):
    queue_id: StrictStr


class GetQueueItemResponsePayload(APIBaseResponse):
    data: Optional[IQueueItem] = None


class GetQueueItemsDateFiltersPayload(BaseModel):
    lte: Optional[StrictStr]
    lt: Optional[StrictStr]
    gt: Optional[StrictStr]
    gte: Optional[StrictStr]


class GetQueueItemsRequestPayload(BaseModel):
    queue_id: StrictStr
    external_id: Optional[StrictStr] = None
    created_at_lte: Optional[StrictStr] = None
    created_at_lt: Optional[StrictStr] = None
    created_at_gte: Optional[StrictStr] = None
    created_at_gt: Optional[StrictStr] = None
    started_at_lte: Optional[StrictStr] = None
    started_at_lt: Optional[StrictStr] = None
    started_at_gte: Optional[StrictStr] = None
    started_at_gt: Optional[StrictStr] = None
    finished_at_lte: Optional[StrictStr] = None
    finished_at_lt: Optional[StrictStr] = None
    finished_at_gte: Optional[StrictStr] = None
    finished_at_gt: Optional[StrictStr] = None
    processing_status_id: Optional[Literal["success", "system_error", "business_exception"]] = None
    processing_exception_id: Optional[StrictStr] = None
    producer_worker_id: Optional[StrictStr] = None
    consumer_worker_id: Optional[StrictStr] = None


class GetQueueItemsResponsePayload(APIBaseResponse):
    data: Optional[IQueueItems] = None


class UpdateQueueItemRequestPayload(BaseModel):
    queue_item_id: StrictStr
    queue_item_processing_status_id: Optional[Literal["system_error", "business_exception", "success"]] = None
    queue_item_processing_status_message: Optional[StrictStr] = None
    queue_item_processing_exception_id: Optional[StrictStr] = None

    @validator("queue_item_processing_status_id", pre=True)
    def queue_item_processing_status_id_field(cls, value, values):
        if values.get("queue_item_processing_exception_id") is None:
            if not value:
                raise ValueError(
                    "When updating a queue item you must provide a valid process status or a queue exception id."
                )
        return value

    @validator("queue_item_processing_exception_id", pre=True, allow_reuse=True)
    def queue_item_processing_exception_id_field(cls, value, values):
        if values.get("queue_item_processing_status_id") is not None:
            if not value:
                raise ValueError(
                    "When updating a queue item you must provide a valid process status or a queue exception id."
                )
        return value

