# /*
#  * Copyright 2023 DataOpen SDK Authors
#  *
#  * Licensed under the Apache License, Version 2.0 (the "License");
#  * you may not use this file except in compliance with the License.
#  * You may obtain a copy of the License at
#  *
#  *     http://www.apache.org/licenses/LICENSE-2.0
#  *
#  * Unless required by applicable law or agreed to in writing, software
#  * distributed under the License is distributed on an "AS IS" BASIS,
#  * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  * See the License for the specific language governing permissions and
#  * limitations under the License.
#  */

import requests
import time
import json
from typing import Union

ParamsValueType = Union[str, int, bool]

class Client:
    METHOD_ALLOWED = ["POST", "GET", "DELETE", "PUT", "PATCH"]
    OPEN_APIS_PATH = "/dataopen/open-apis"

    def __init__(
        self,
        app_id: str,
        app_secret: str,
        url: Union[str, None] = "https://analytics.volcengineapi.com",
        expiration: Union[str, None] = "1800"
    ):
        self.app_id = app_id
        self.app_secret = app_secret
        self.url = url
        self.expiration = expiration
        self._ttl = 0
        self._access_token = ""
        self._token_time = 0

    def request(self, service_url: str, method: str, headers: dict, params: dict, body: dict) -> dict:
        upper_case_method = method.upper()

        if not self._access_token or not self._valid_token():
            self.get_token()

        new_headers = {
            "Authorization": self._access_token,
            "Content-Type": "application/json",
            "x-sdk-source": "python"
        }

        for key in headers:
            new_headers[key] = headers[key]

        completed_url = f"{self.url}{service_url}"
        query_url = self._joint_query(completed_url, params)

        if upper_case_method == "GET":
            resp = requests.get(query_url, headers=new_headers).json()
        elif upper_case_method == "POST":
            resp = requests.post(
                query_url, headers=new_headers, data=json.dumps(body)).json()
        elif upper_case_method == "PUT":
            resp = requests.put(
                query_url, headers=new_headers, data=json.dumps(body)).json()
        elif upper_case_method == "DELETE":
            resp = requests.delete(
                query_url, headers=new_headers, data=json.dumps(body)).json()
        elif upper_case_method == "PATCH":
            resp = requests.patch(
                query_url, headers=new_headers, data=json.dumps(body)).json()
        else:
            raise ValueError("Invalid request method")

        return resp

    def is_authenticated(self) -> bool:
        return self._access_token != ""

    def get_token(self):
        authorization_url = f"{self.OPEN_APIS_PATH}/v1/authorization"
        print("authorization_url", authorization_url)
        completed_url = f"{self.url}/{authorization_url}"

        data = {
            "app_id": self.app_id,
            "app_secret": self.app_secret,
        }

        resp = requests.post(completed_url, headers={
                             "Content-Type": "application/json", "x-sdk-source": "python"}, data=json.dumps(data)).json()

        token_time = time.time()

        if resp.get('code') == 200 and 'data' in resp:
            self._ttl = resp['data']['ttl']
            self._token_time = token_time
            self._access_token = resp['data']['access_token']

    @staticmethod
    def _joint_query(url: str, params: dict) -> str:
        paramStr = "&".join([f"{key}={val}" for key, val in params.items()])
        return f"{url}?{paramStr}"

    def _valid_token(self) -> bool:
        current_time = time.time()

        if current_time - self._token_time > self._ttl:
            return False

        return True
