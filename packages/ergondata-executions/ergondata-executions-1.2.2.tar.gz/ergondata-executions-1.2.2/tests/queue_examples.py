import os

from ergondata_executions.controllers.auth.controller import AuthController
from ergondata_executions.controllers.auth.interfaces import AuthRequestPayload

from ergondata_executions.controllers.queue.controller import QueueController
from ergondata_executions.controllers.queue.interfaces import *

auth = AuthRequestPayload(
    username=os.getenv('CLIENT_OWNER_API_USERNAME'),
    password=os.getenv('CLIENT_OWNER_API_PASSWORD')
)
api_client = AuthController(auth=auth, logging=True, timeout=20)
controller = QueueController(api_client=api_client)

''' CREATE QUEUE '''

queue_item_created_email_recipients = [
    IEmailRecipient(
        email="daniel.vossos@ergondata.com.br",
        pre_header_name="Daniel"
    )
]

queue_item_started_email_recipients = [
    IEmailRecipient(
        email="daniel.vossos@ergondata.com.br",
        pre_header_name="Daniel"
    )
]

queue_item_succeeded_email_recipients = [
    IEmailRecipient(
        email="daniel.vossos@ergondata.com.br",
        pre_header_name="Daniel"
    )
]

queue_item_failed_email_recipients = [
    IEmailRecipient(
        email="daniel.vossos@ergondata.com.br",
        pre_header_name="Daniel"
    )
]

create_queue_request = CreateQueueRequestPayload(
    process_id="324c8d35-9ca9-484d-ac71-d372b8f82019",
    queue_name="Quitação de Contrato",
    queue_description="Items para quitacao de contrato",
    allow_to_include_repeated_queue_item=False,
    queue_item_max_retries_within_execution=1,
    queue_item_max_retries_outside_execution=5,
    queue_item_created_email_integration=True,
    queue_item_started_email_integration=True,
    queue_item_succeeded_email_integration=True,
    queue_item_failed_email_integration=True,
    queue_item_created_email_recipients=queue_item_created_email_recipients,
    queue_item_failed_email_recipients=queue_item_failed_email_recipients,
    queue_item_succeeded_email_recipients=queue_item_succeeded_email_recipients,
    queue_item_started_email_recipients=queue_item_started_email_recipients
)
create_queue_response = controller.create_queue(params=create_queue_request)


''' DELETE QUEUE '''
delete_queue_request = DeleteQueueRequestPayload(
    queue_id="3b5c53b3-a28c-4243-9b34-fd1f0614fb4b"
)
delete_queue_response = controller.delete_queue(params=delete_queue_request)


''' GET QUEUES '''

get_queues_request = GetQueuesRequestPayload(
    process_id="324c8d35-9ca9-484d-ac71-d372b8f82019"
)
get_queues_response = controller.get_queues(params=get_queues_request)


''' UPDATE QUEUE '''

queue_item_created_email_recipients = [
    IEmailRecipient(
        email="daniel.vossos@ergondata.com.br",
        pre_header_name="Daniel"
    )
]

queue_item_created_email_recipients_integration = UpdateQueueEmailRecipientsPayload(
    action="remove",
    emails=queue_item_created_email_recipients
)

queue_item_created_email_integration = UpdateQueueEmailIntegrationPayload(
    active=False,
    recipients=queue_item_created_email_recipients_integration
)

queue_item_started_email_recipients = [
    IEmailRecipient(
        email="jorge.vossos@ergondata.com.br",
        pre_header_name="Jorge"
    )
]

queue_item_started_email_recipients_integration = UpdateQueueEmailRecipientsPayload(
    action="add",
    emails=queue_item_started_email_recipients
)

queue_item_started_email_integration = UpdateQueueEmailIntegrationPayload(
    active=True,
    recipients=queue_item_started_email_recipients_integration
)

queue_item_succeeded_email_recipients = [
    IEmailRecipient(
        email="jorge.vossos@ergondata.com.br",
        pre_header_name="Jorge"
    )
]

queue_item_succeeded_email_recipients_integration = UpdateQueueEmailRecipientsPayload(
    action="add",
    emails=queue_item_succeeded_email_recipients
)

queue_item_succeeded_email_integration = UpdateQueueEmailIntegrationPayload(
    active=True,
    recipients=queue_item_succeeded_email_recipients_integration
)

queue_item_failed_email_recipients = [
    IEmailRecipient(
        email="jorge.vossos@ergondata.com.br",
        pre_header_name="Jorge"
    )
]

queue_item_failed_email_recipients_integration = UpdateQueueEmailRecipientsPayload(
    action="overwrite",
    emails=queue_item_failed_email_recipients
)

queue_item_failed_email_integration = UpdateQueueEmailIntegrationPayload(
    active=True,
    recipients=queue_item_failed_email_recipients_integration
)

email_integration = UpdateQueueEmailIntegration(
    queue_item_created=queue_item_created_email_integration,
    queue_item_started=queue_item_started_email_integration,
    queue_item_succeeded=queue_item_succeeded_email_integration,
    queue_item_failed=queue_item_failed_email_integration,
)

update_queue_request = UpdateQueueRequestPayload(
    queue_id="f3cf9181-b43a-4d59-9a6a-e33cc8f13382",
    queue_name="Teste Rename Fila",
    allow_to_include_repeated_queue_item=True,
    queue_item_max_retries_within_execution=10,
    queue_item_max_retries_outside_execution=20,
    email_integration=email_integration
)
update_queue_response = controller.update_queues(params=update_queue_request)