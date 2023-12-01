import logging
import time

import requests
from requests import Response

logging.basicConfig(level=logging.INFO)


class RetryRequest:
    def __init__(self, retries=70, sleep_time_sec=5, logs=True) -> None:
        self.retries = retries
        self.sleep_time_sec = sleep_time_sec
        self.logs = logs

    def _request(self, url, method, **kwargs) -> Response:
        customer_uuid = kwargs.pop("customer_uuid") if "customer_uuid" in kwargs else None
        for index in range(1, self.retries + 1):
            if self.logs:
                logging.info(f"[RequestRetry][{customer_uuid}] endpoint: {url} args: {kwargs} attempt: {index}")
            response: Response = method(url=url, **kwargs)
            if response.status_code not in [423, 504]:
                break
            time.sleep(self.sleep_time_sec)
        if self.logs and response.status_code not in [200, 201]:
            logging.error(
                f"[RequestRetry][{customer_uuid}] Error Response: {response.status_code} - {response.content}"
            )
        return response

    def get(self, url, **kwargs) -> Response:
        method = requests.get
        return self._request(url, method, **kwargs)

    def post(self, url, **kwargs) -> Response:
        method = requests.post
        return self._request(url, method, **kwargs)

    def put(self, url, **kwargs) -> Response:
        method = requests.put
        return self._request(url, method, **kwargs)

    def delete(self, url, **kwargs) -> Response:
        method = requests.delete
        return self._request(url, method, **kwargs)

    def retry_request(
        self,
        endpoint: str,
        data: dict,
        customer_uuid: str,
        headers: dict,
        method: str,
        params: dict = None,
        logs: bool = True,
    ):
        if params is None:
            params = {}

        if logs:
            logging.info(f"[Retry request] Retry call ingestion. {customer_uuid}. endpoint: {endpoint}")

        control = 0
        total = 70
        req = None
        while control < total:
            if control > 0:
                time.sleep(5)

            control += 1
            if logs:
                logging.info(f"[Retry request][{customer_uuid}][{endpoint}] Retry {control} of {total}")

            if method == "GET":
                req = requests.get(endpoint, params=params, headers=headers)
            elif method == "POST":
                req = requests.post(endpoint, json=data, headers=headers, params=params)
            elif method == "PUT":
                req = requests.put(endpoint, json=data, headers=headers, params=params)
            else:
                req = requests.patch(endpoint, json=data, headers=headers, params=params)

            if req.status_code == 423 or req.status_code == 504:
                continue
            elif req.status_code == 200 or req.status_code == 201:
                if logs:
                    logging.info(f"[Retry request][{customer_uuid}] Retry call accepted. Endpoint: {endpoint}")
                break
            else:
                if logs:
                    logging.error(
                        f"[Retry request][{customer_uuid}] Error to retry call. Error: {req}. Endpoint: {endpoint}. Params: {data}"
                    )
                return False, {}

        if req.status_code == 423 or req.status_code == 504:
            if logs:
                logging.error(
                    f"[Retry request][{customer_uuid}] Error to retry call after loop. Error: {req}. Endpoint: {endpoint}. Params: {data}"
                )
            return False, {}

        return True, req.json()

    def response_checker(
        self,
        req,
        customer_uuid: str,
        method: str,
        url: str,
        headers: dict = None,
        params: dict = None,
        data: dict = None,
        process: str = "",
    ):
        if headers is None:
            headers = {}
        if data is None:
            data = {}
        if params is None:
            params = {}

        if req.status_code == 200:
            payload = req.json()

            return payload

        if req.status_code == 423 or req.status_code == 504:
            status, payload = self.retry_request(
                endpoint=url,
                customer_uuid=customer_uuid,
                data=data,
                params=params,
                headers=headers,
                method=method,
            )

            if not status:
                logging.error(f"[{process}][{customer_uuid}] Error to call hubspot ingestion {req}")
                raise Exception("Endpoint unavailable")

            return payload

        else:
            logging.error(f"[{process}][{customer_uuid}] Error to call hubspot ingestion {req}. Status code: {req}")
            raise Exception("Endpoint unavailable")
