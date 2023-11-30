import datetime

from pydantic import BaseModel, StrictInt, StrictBool, StrictStr
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
    user_defined_id: StrictStr
    item: Any
    queue: Optional[IQueue]
    processing_status_id: Optional[StrictStr]
    processing_status_message: Optional[StrictStr]
    processing_exception: Optional[IQueueProcessingException]
    created_at: Optional[datetime.datetime]
    started_at: Optional[datetime.datetime]
    finished_at: Optional[datetime.datetime]


class IQueueItems(BaseModel):
    queue_items: List[IQueueItem] = []


class CreateQueueRequestPayload(BaseModel):
    process_id: StrictStr
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


class CreateQueueResponsePayload(APIBaseResponse):
    queue_id: Optional[StrictStr] = None


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
    queue_description: Optional[StrictStr] = None
    email_integration: Optional[UpdateQueueEmailIntegration]
    allow_to_include_repeated_queue_item: Optional[StrictBool]
    queue_item_max_retries_within_execution: Optional[StrictInt]
    queue_item_max_retries_outside_execution: Optional[StrictInt]


class CreateQueueItemRequestPayload(BaseModel):
    queue_item_user_generated_id: StrictStr
    queue_id: StrictStr
    queue_item: object


class CreateQueueItemResponsePayload(APIBaseResponse):
    queue_item_api_generated_id: StrictStr


class GetQueueItemRequestPayload(BaseModel):
    queue_id: StrictStr


class GetQueueItemResponsePayload(APIBaseResponse):
    data: Union[IQueueItem, None]



class GetQueueItemsDateFiltersPayload(BaseModel):
    lte: Optional[StrictStr]
    lt: Optional[StrictStr]
    gt: Optional[StrictStr]
    gte: Optional[StrictStr]


class GetQueueItemsRequestPayload(BaseModel):
    queue_id: StrictStr
    created_at: Optional[GetQueueItemsDateFiltersPayload]
    started_at: Optional[GetQueueItemsDateFiltersPayload]
    finished_at: Optional[GetQueueItemsDateFiltersPayload]
    processing_status_id: Optional[Literal["success", "system_error", "business_exception"]]
    processing_exception_id: Optional[StrictStr]


class GetQueueItemsResponsePayload(APIBaseResponse):
    data: IQueueItems


class UpdateQueueItemRequestPayload(BaseModel):
    queue_item_id: Optional[StrictStr]
    queue_item_processing_status_id: Literal["system_error", "business_exception", "success"]
    queue_item_processing_status_message: Optional[StrictStr] = None
    queue_item_processing_exception_id: Optional[StrictStr] = None
