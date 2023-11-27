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


from .sections import Account
from .sections import Article
from .sections import Country
from .sections import Currency
from .sections import Language
from .sections import Notification
from .sections import Role
from .sections import Session
from .sections import Timezone


sections = [
    Account,
    Article,
    Country,
    Currency,
    Language,
    Notification,
    Role,
    Session,
    Timezone,
]


class MyBodyApiClient:
    account: Account
    article: Article
    country: Country
    currency: Currency
    language: Language
    notification: Notification
    role: Role
    session: Session
    timezone: Timezone

    def __init__(self, token: str = None):
        for section in sections:
            exec(f'self.{section.__name__.lower()} = section(token="{token}")')
