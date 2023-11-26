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


from mybody_api_client.sections.base import BaseSection, RequestTypes


class Article(BaseSection):
    prefix = 'articles'

    async def get(self, article_id, language=None):
        path = f'/{article_id}/get'
        response = await self.request(
            type_=RequestTypes.GET,
            path=path,
            token_required=False,
            parameters={
                'language': language,
            },
        )
        return response

    async def create(self, name):
        path = '/create'
        response = await self.request(
            type_=RequestTypes.POST,
            path=path,
            parameters={
                'name': name,
            },
        )

        return response

    async def translation_create(self, articles_id, language):
        path = f'/{articles_id}/translations/create'
        response = await self.request(
            type_=RequestTypes.POST,
            path=path,
            parameters={
                'language': language,
            },
        )
        return response

    async def update(self, articles_id, is_hide=None):
        path = f'/{articles_id}/update'
        response = await self.request(
            type_=RequestTypes.POST,
            path=path,
            parameters={
                'is_hide': is_hide,
            },
        )
        return response

    async def update_md(self, articles_id, md, language=None):
        path = f'/{articles_id}/update/md'
        response = await self.request(
            type_=RequestTypes.POST,
            path=path,
            parameters={
                'language': language,
                'md': md,
            },
        )
        return response
