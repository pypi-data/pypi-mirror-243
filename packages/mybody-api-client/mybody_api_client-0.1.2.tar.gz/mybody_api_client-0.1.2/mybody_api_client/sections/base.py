#
# (c) 2023, Yegor Yakubovich, yegoryakubovich.com, personal@yegoryakybovich.com
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#


from types import SimpleNamespace

import httpx
from furl import furl


HOST = 'api.mybody.by'


class RequestTypes:
    GET = 'get'
    POST = 'post'


class BaseSection:
    prefix: str = ''
    token: str

    def __init__(self, token: str = None):
        self.token = token

    async def create_url(self, path: str, parameters: dict) -> str:
        f = furl(scheme='https', netloc=HOST, path=self.prefix + path)
        f.set(args=parameters)
        return f.url

    async def request(
            self,
            path: str,
            type_: str = RequestTypes.GET,
            token_required: bool = True,
            parameters: dict = None,
    ):
        parameters = parameters or {}
        json = {}
        if token_required or self.token:
            parameters['token'] = self.token

        if type_ == RequestTypes.POST:
            json = parameters
            parameters = {}

        url = await self.create_url(
            path=path,
            parameters=parameters,
        )

        async with httpx.AsyncClient() as client:
            if type_ == RequestTypes.GET:
                response = await client.get(url)
            elif type_ == RequestTypes.POST:
                response = await client.post(url, json=json)

        response_json = response.json()
        return SimpleNamespace(**response_json)
