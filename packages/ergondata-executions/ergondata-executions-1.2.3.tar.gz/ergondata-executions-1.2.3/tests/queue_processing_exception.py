import os
from ergondata_executions.controllers.auth.controller import AuthController
from ergondata_executions.controllers.auth.interfaces import AuthRequestPayload

from ergondata_executions.controllers.queue_processing_exception.controller import QueueProcessingExceptionController
from ergondata_executions.controllers.queue_processing_exception.interfaces import *

auth = AuthRequestPayload(
    username=os.getenv('CLIENT_OWNER_API_USERNAME'),
    password=os.getenv('CLIENT_OWNER_API_PASSWORD')
)
api_client = AuthController(auth=auth, logging=True, timeout=20)
controller = QueueProcessingExceptionController(api_client=api_client)

queue_processing_exception_email_recipients = [
    IEmailRecipient(
        email="lorenzo@ergondata.com.br",
        pre_header_name="Lore"
    ),
    IEmailRecipient(
        email="lorenzo@ergondata.com.br",
        pre_header_name="Lore"
    )
]

create_queue_exception_request = CreateQueueProcessingExceptionRequestPayload(
    queue_id="368d2cd7-a173-4667-9cae-90bce75d822c",
    queue_processing_exception_name="Falha ao realizar login no portal da KMM.",
    queue_processing_exception_type="system_error",
    queue_processing_exception_description="Esta exceção é gerada no momento em que o robô naão consegue efetuar login no portal após retentivas.",
    queue_processing_exception_email_integration=True,
    queue_processing_exception_email_recipients=queue_processing_exception_email_recipients
)
create_queue_exception_response = controller.create_queue_processing_exception(params=create_queue_exception_request)


delete_queue_exception_request = DeleteQueueProcessingExceptionRequestPayload(
    queue_processing_exception_id="5d0bee3a-7ef6-49d2-971e-f6ab0001ea83"
)
delete_queue_exception_response = controller.delete_queue_processing_exception(params=delete_queue_exception_request)

get_queue_processing_exceptions_request = GetQueueProcessingExceptionsRequestPayload(
    queue_id="368d2cd7-a173-4667-9cae-90bce75d822c"
)
get_queue_processing_exceptions_response = controller.get_queue_processing_exceptions(params=get_queue_processing_exceptions_request)

emails_recipients = [
    IEmailRecipient(
        email="robert@ergondata.com.br",
        pre_header_name="Lorenzo"
    ),
    IEmailRecipient(
        email="emmanuel@ergondata.com.br",
        pre_header_name="Lorenzo"
    )
]

email_recipients_payload = UpdateEmailRecipientsIntegrationPayload(
    action="overwrite",
    emails=emails_recipients
)

email_integration = UpdateEmailIntegrationPayload(
    active=True,
    recipients=email_recipients_payload
)

update_queue_processing_exception_request = UpdateQueueProcessingExceptionRequestPayload(
    queue_processing_exception_id="509e252a-0fcc-46dc-a0c3-b0af3ae3a75b",
    queue_processing_exception_name="PLANILHA SEM DADOSssss",
    queue_processing_exception_description="Teste de renomeamento",
    queue_processing_exception_email_integration=email_integration
)
update_queue_processing_exception_response = controller.update_queue_processing_exceptions(
    params=update_queue_processing_exception_request
)

