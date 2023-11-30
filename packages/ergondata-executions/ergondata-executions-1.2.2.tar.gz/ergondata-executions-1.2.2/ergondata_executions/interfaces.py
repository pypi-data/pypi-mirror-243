from pydantic import BaseModel, StrictStr, StrictBool
from typing import Union, Optional, Literal, List


class APIBaseResponse(BaseModel):
    status: Literal["success", "error"]
    message: StrictStr
    error_messages: Optional[List[object]] = None


class IEmailRecipient(BaseModel):
    email: StrictStr
    pre_header_name: StrictStr


class IEmailIntegrationData(BaseModel):
    active: StrictBool
    recipients: Union[List[IEmailRecipient], None] = None


class UpdateEmailRecipientsPayload(BaseModel):
    action: Literal["overwrite", "add", "remove"]
    emails: List[IEmailRecipient]
