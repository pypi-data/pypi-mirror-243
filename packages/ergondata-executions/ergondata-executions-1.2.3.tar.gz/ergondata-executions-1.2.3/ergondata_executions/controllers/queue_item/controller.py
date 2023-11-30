import requests
from ergondata_executions.controllers.queue_item.interfaces import *
from ergondata_executions.controllers.auth.controller import AuthController


class QueueItemController:

    CREATE_QUEUE_ITEM_URL = 'create/database/process/queue/item'
    RESET_QUEUE_ITEM_URL = 'reset/database/process/queue/item'
    GET_QUEUE_ITEM_URL = 'get/database/process/queue/{0}/item'
    GET_QUEUE_ITEMS_URL = 'get/database/process/queue/{0}/items'
    UPDATE_QUEUE_ITEM_URL = 'update/database/process/queue/item'

    def __init__(self, api_client: AuthController):
        self.api_client = api_client

    def create_queue_item(self, params: CreateQueueItemRequestPayload) -> CreateQueueItemResponsePayload:

        self.api_client.log_info(f"Creating queue item.")

        try:

            res = requests.post(
                url=f"{self.api_client.ROOT_URL}{self.CREATE_QUEUE_ITEM_URL}",
                json=params.model_dump(),
                headers=self.api_client.exec_header,
                timeout=self.api_client.timeout
            )

            response_payload = CreateQueueItemResponsePayload(**res.json())
            if res.status_code == 200:
                self.api_client.log_info(response_payload)
            else:
                self.api_client.log_error(response_payload)
            return response_payload

        except BaseException as e:

            self.api_client.log_error(f"Failed to create queue item: {e}.")

            response_payload = CreateQueueItemResponsePayload(
                status="error",
                message=str(e)
            )

            return response_payload


    def update_queue_item(self, params: UpdateQueueItemRequestPayload) -> APIBaseResponse:

        self.api_client.log_info(f"Updating queue item.")

        try:

            res = requests.put(
                url=f"{self.api_client.ROOT_URL}{self.UPDATE_QUEUE_ITEM_URL}",
                json=params.model_dump(),
                headers=self.api_client.exec_header,
                timeout=self.api_client.timeout
            )

            response_payload = APIBaseResponse(**res.json())
            if res.status_code == 200:
                self.api_client.log_info(response_payload)
            else:
                self.api_client.log_error(response_payload)
            return response_payload

        except BaseException as e:

            self.api_client.log_error(f"Failed to update queue item: {e}.")

            response_payload = APIBaseResponse(
                status="error",
                message=str(e)
            )

            return response_payload

    def reset_queue_item(self):

        self.api_client.log_info(f"Resetting queue item.")

        try:

            res = requests.post(
                url=f"{self.api_client.ROOT_URL}{self.RESET_QUEUE_ITEM_URL}",
                headers=self.api_client.auth_header,
                timeout=self.api_client.timeout
            )

            response_payload = APIBaseResponse(**res.json())
            if res.status_code == 200:
                self.api_client.log_info(response_payload)
            else:
                self.api_client.log_error(response_payload)
            return response_payload

        except BaseException as e:

            self.api_client.log_error(f"Failed to reset queue item: {e}.")

            response_payload = CreateQueueItemResponsePayload(
                status="error",
                message=str(e)
            )

            return response_payload
        pass

    def get_queue_item(self, params: GetQueueItemRequestPayload) -> GetQueueItemResponsePayload:

        self.api_client.log_info(f"Getting next queue item.")

        try:

            res = requests.get(
                url=f"{self.api_client.ROOT_URL}{self.GET_QUEUE_ITEM_URL.format(params.queue_id)}",
                headers=self.api_client.exec_header,
                timeout=self.api_client.timeout
            )

            response_payload = GetQueueItemResponsePayload(**res.json())
            if res.status_code == 200:
                self.api_client.log_info(response_payload)
            else:
                self.api_client.log_error(response_payload)
            return response_payload

        except BaseException as e:

            self.api_client.log_error(f"Failed to get next queue item: {e}.")

            response_payload = GetQueueItemResponsePayload(
                status="error",
                message=str(e)
            )

            return response_payload
        pass

    def get_queue_items(self, params: GetQueueItemsRequestPayload) -> GetQueueItemsResponsePayload:

        self.api_client.log_info(f"Getting queue items.")

        try:

            get_queue_items_url = self.GET_QUEUE_ITEMS_URL.format(params.queue_id) + '?'

            get_queue_items_url = get_queue_items_url + f'created_at_lt={params.created_at_lt}&' if params.created_at_lt else get_queue_items_url
            get_queue_items_url = get_queue_items_url + f'created_at_lte={params.created_at_lte}&' if params.created_at_lte else get_queue_items_url
            get_queue_items_url = get_queue_items_url + f'created_at_gt={params.created_at_gt}&' if params.created_at_gt else get_queue_items_url
            get_queue_items_url = get_queue_items_url + f'created_at_gte={params.created_at_gte}&' if params.created_at_gte else get_queue_items_url
            get_queue_items_url = get_queue_items_url + f'started_at_lt={params.started_at_lt}&' if params.started_at_lt else get_queue_items_url
            get_queue_items_url = get_queue_items_url + f'started_at_lte={params.started_at_lte}&' if params.started_at_lte else get_queue_items_url
            get_queue_items_url = get_queue_items_url + f'started_at_gt={params.started_at_gt}&' if params.started_at_gt else get_queue_items_url
            get_queue_items_url = get_queue_items_url + f'started_at_gte={params.started_at_gte}&' if params.started_at_gte else get_queue_items_url
            get_queue_items_url = get_queue_items_url + f'finished_at_lte={params.finished_at_lte}&' if params.finished_at_lte else get_queue_items_url
            get_queue_items_url = get_queue_items_url + f'finished_at_lt={params.finished_at_lt}&' if params.finished_at_lt else get_queue_items_url
            get_queue_items_url = get_queue_items_url + f'finished_at_gt={params.finished_at_gt}&' if params.finished_at_gt else get_queue_items_url
            get_queue_items_url = get_queue_items_url + f'finished_at_gte={params.finished_at_gte}&' if params.finished_at_gte else get_queue_items_url
            get_queue_items_url = get_queue_items_url + f'processing_status_id={params.processing_status_id}&' if params.processing_status_id else get_queue_items_url
            get_queue_items_url = get_queue_items_url + f'processing_exception_id={params.processing_exception_id}&' if params.processing_exception_id else get_queue_items_url
            get_queue_items_url = get_queue_items_url + f'producer_worker_id={params.producer_worker_id}&' if params.producer_worker_id else get_queue_items_url
            get_queue_items_url = get_queue_items_url + f'consumer_worker_id={params.consumer_worker_id}&' if params.consumer_worker_id else get_queue_items_url

            res = requests.get(
                url=f"{self.api_client.ROOT_URL}{get_queue_items_url}",
                headers=self.api_client.auth_header,
                timeout=self.api_client.timeout
            )
            response_payload = GetQueueItemsResponsePayload(**res.json())

            if res.status_code == 200:
                self.api_client.log_info(response_payload)
            else:
                self.api_client.log_error(response_payload)
            return response_payload

        except BaseException as e:

            self.api_client.log_error(f"Failed to get queue items {e}.")

            return GetQueueItemsResponsePayload(
                status="error",
                message=str(e)
            )