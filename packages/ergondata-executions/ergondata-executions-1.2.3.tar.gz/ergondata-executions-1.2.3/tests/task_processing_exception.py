from ergondata_executions.controllers.auth.controller import AuthController
from ergondata_executions.controllers.auth.interfaces import AuthRequestPayload

from ergondata_executions.controllers.task_processing_exception.controller import TaskProcessingExceptionController
from ergondata_executions.controllers.task_processing_exception.interfaces import *

auth = AuthRequestPayload(
    username="",
    password=""
)
api_client = AuthController(auth=auth, logging=True, timeout=20)
controller = TaskProcessingExceptionController(api_client=api_client)

emails_recipients = [
    IEmailRecipient(
        email="daniel.vossos@ergondata.com.br",
        pre_header_name="Daniel"
    )
]

create_task_exception_request = CreateTaskProcessingExceptionRequestPayload(
    task_id="e503f7fa-f776-4ed0-b938-5ba5873c2c1c",
    task_processing_exception_status_id="business_exception",
    task_processing_exception_name="Planilha Sharepoint Vazia",
    task_processing_exception_description="Esta exceção é gerada quando o robô baixa a planilha com sucesso mas ela está sem dados.",
    task_processing_exception_email_integration=True,
    task_processing_exception_email_recipients=emails_recipients
)
create_task_exception_response = controller.create_task_processing_exception(params=create_task_exception_request)

get_task_processing_exceptions_request = GetTaskProcessingExceptionsRequestPayload(
    task_id="e503f7fa-f776-4ed0-b938-5ba5873c2c1c"
)
get_task_processing_exceptions_response = controller.get_task_processing_exceptions(params=get_task_processing_exceptions_request)

'''

'''

'''
delete_task_exception_request = DeleteTaskProcessingExceptionRequestPayload(
    task_processing_exception_id="0c1284c6-78c8-42e5-aa7a-b05254b455a3"
)
delete_task_exception_response = controller.delete_task_processing_exception(params=delete_task_exception_request)
'''

'''
'''

emails_recipients = [
    IEmailRecipient(
        email="daniel.vossos@ergondata.com.br",
        pre_header_name="Daniel"
    )
]

email_recipients_payload = UpdateEmailRecipientsIntegrationPayload(
    action="add",
    emails=emails_recipients
)

email_integration = UpdateEmailIntegrationPayload(
    active=True,
    recipients=email_recipients_payload
)

update_task_processing_exception_request = UpdateTaskProcessingExceptionRequestPayload(
    task_processing_exception_id="09e476c2-f22c-4f66-b487-161a448fb301",
    task_processing_exception_name="PLANILHA SEM DADOS",
    task_processing_exception_description="Teste de renomeamento",
    task_processing_exception_email_integration=email_integration
)

update_task_processing_exception_response = controller.update_task_processing_exceptions(
    params=update_task_processing_exception_request
)

