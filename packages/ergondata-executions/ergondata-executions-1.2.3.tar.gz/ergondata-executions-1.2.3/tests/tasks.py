import os
from ergondata_executions.controllers.auth.controller import AuthController
from ergondata_executions.controllers.auth.interfaces import AuthRequestPayload

from ergondata_executions.controllers.task.controller import TaskController
from ergondata_executions.controllers.task.interfaces import *


auth = AuthRequestPayload(
    username=os.getenv('CLIENT_OWNER_API_USERNAME'),
    password=os.getenv('CLIENT_OWNER_API_PASSWORD')
)

api_client = AuthController(auth=auth, logging=True, timeout=20)

task_controller = TaskController(api_client=api_client)

''' CREATE TASK '''
task_started_email_recipients = [
    IEmailRecipient(
        email="lucas.leite@ergondata.com.br",
        pre_header_name="Lucas"
    ),
    IEmailRecipient(
        email="lorenzo@ergondata.com.br",
        pre_header_name="Lorenzo"
    ),
    IEmailRecipient(
        email="daniel.vossos@ergondata.com.br",
        pre_header_name="Daniel"
    )
]

task_succeeded_email_recipients = [
    IEmailRecipient(
        email="lucas.leite@ergondata.com.br",
        pre_header_name="Lucas"
    ),
    IEmailRecipient(
        email="lorenzo@ergondata.com.br",
        pre_header_name="Lorenzo"
    ),
    IEmailRecipient(
        email="daniel.vossos@ergondata.com.br",
        pre_header_name="Daniel"
    )
]

task_failed_emailed_recipients = [
    IEmailRecipient(
        email="lucas.leite@ergondata.com.br",
        pre_header_name="Lucas"
    ),
    IEmailRecipient(
        email="lorenzo@ergondata.com.br",
        pre_header_name="Lorenzo"
    ),
    IEmailRecipient(
        email="daniel.vossos@ergondata.com.br",
        pre_header_name="Daniel"
    )
]

create_task_request = CreateTaskRequestPayload(
    process_id="324c8d35-9ca9-484d-ac71-d372b8f82019",
    task_name="Perfomer Geracão de Contrato",
    task_description="Essa task le os dados da fila de geraçaão de contrato e tenta gerar o número de contrato. Se conseguir, coloca na fila de quitação.",
    task_type="performer-and-dispatcher",
    task_started_email_integration=True,
    task_succeeded_email_integration=True,
    task_failed_email_integration=True,
    task_started_email_recipients=task_started_email_recipients,
    task_succeeded_email_recipients=task_succeeded_email_recipients,
    task_failed_email_recipients=task_failed_emailed_recipients
)

create_task_response = task_controller.create_task(params=create_task_request)

''' DELETE TASK '''
delete_task_request = DeleteTaskRequestPayload(
    task_id='d3547abb-0548-40eb-90e6-2170058b4a91'
)
delete_task_response = task_controller.delete_task(params=delete_task_request)


''' GET TASKS '''
get_tasks_request = GetTasksRequestPayload(process_id="324c8d35-9ca9-484d-ac71-d372b8f82019")
get_tasks_response = task_controller.get_tasks(params=get_tasks_request)


''' UPDATE TASK '''
task_failed_emails = [
    IEmailRecipient(
        email="emmanuel@ergondata.com.br",
        pre_header_name="Emmanuel"
    ),
    IEmailRecipient(
        email="maria@ergondata.com.br",
        pre_header_name="Maria"
    ),
]

task_failed_email_recipients_payload = UpdateTaskEmailRecipientsPayload(
    action="add",
    emails=task_failed_emails
)

task_failed_email_integration = UpdateTaskEmailIntegrationPayload(
    active=True,
    recipients=task_failed_email_recipients_payload
)

task_succeeded_emails = [
    IEmailRecipient(
        email="emmanuel@ergondata.com.br",
        pre_header_name="Emmanuel"
    ),
    IEmailRecipient(
        email="maria@ergondata.com.br",
        pre_header_name="Maria"
    ),
]

task_succeeded_email_recipients_payload = UpdateTaskEmailRecipientsPayload(
    action="remove",
    emails=task_succeeded_emails
)

task_succeeded_email_integration = UpdateTaskEmailIntegrationPayload(
    active=True,
    recipients=task_succeeded_email_recipients_payload
)

task_started_emails = [
    IEmailRecipient(
        email="emmanuel@ergondata.com.br",
        pre_header_name="Emmanuel"
    ),
    IEmailRecipient(
        email="maria@ergondata.com.br",
        pre_header_name="Maria"
    ),
]

task_started_email_recipients_payload = UpdateTaskEmailRecipientsPayload(
    action="overwrite",
    emails=task_started_emails
)

task_started_email_integration = UpdateTaskEmailIntegrationPayload(
    active=True,
    recipients=task_started_email_recipients_payload
)

task_email_integration = UpdateTaskEmailIntegration(
    task_started=task_started_email_integration,
    task_succeeded=task_succeeded_email_integration,
    task_failed=task_failed_email_integration
)

update_task_request = UpdateTaskRequestPayload(
    task_id="367a9289-b9d2-4bea-929a-4ce5e6c539ac",
    task_name="Novo processo",
    task_description="Teste de rename",
    task_email_integration=task_email_integration
)
update_task_response = task_controller.update_tasks(params=update_task_request)







