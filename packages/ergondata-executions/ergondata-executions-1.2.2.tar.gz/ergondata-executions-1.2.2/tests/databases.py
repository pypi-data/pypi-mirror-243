import os
from dotenv import load_dotenv

from ergondata_executions.controllers.auth.controller import AuthController
from ergondata_executions.controllers.auth.interfaces import AuthRequestPayload

from ergondata_executions.controllers.database.controller import DBController
from ergondata_executions.controllers.database.interfaces import *

load_dotenv()

auth = AuthRequestPayload(
    username=os.getenv('CLIENT_OWNER_API_USERNAME'),
    password=os.getenv('CLIENT_OWNER_API_PASSWORD'),
    client_id=os.getenv('CLIENT_OWNER_API_CLIENT_ID')
)

api_client = AuthController(auth=auth, logging=True, timeout=20)
db_controller = DBController(api_client)

'''
get_dbs_response = db_controller.get_databases()

create_database_request = CreateDatabaseRequestPayload(
    database_name="Operaçoes"
)
create_db_response = db_controller.create_database(params=create_database_request)

delete_database_request = DeleteDatabaseRequestPayload(
    database_id='84da07ab-e46c-4f1b-8495-90fc78977b17'
)
delete_database_response = db_controller.delete_database(params=delete_database_request)

update_database_request = UpdateDatabaseRequestPayload(
    database_id='',
    database_name=''
)
update_database_response = db_controller.update_database(params=update_database_request)
'''
create_db_member_request = CreateDatabaseMemberRequestPayload(
    database_id="2cfef6f3-22c6-4400-bb13-7d95850f4bef",
    database_member_email="lorenzo@ergondata.com.br",
    database_member_username="lorenzo.freto"
)
create_db_member_response = db_controller.create_database_member(params=create_db_member_request)

get_db_members_request = GetDatabaseMembersRequestPayload(
    database_id="2cfef6f3-22c6-4400-bb13-7d95850f4bef"
)
get_db_members_response = db_controller.get_database_members(params=get_db_members_request)

delete_database_member_request = DeleteDatabaseMemberRequestPayload(
    database_member_id="c54552c3-0475-4c00-a1dd-7c9baa067085"
)
delete_database_member_response = db_controller.delete_database_member(params=delete_database_member_request)


