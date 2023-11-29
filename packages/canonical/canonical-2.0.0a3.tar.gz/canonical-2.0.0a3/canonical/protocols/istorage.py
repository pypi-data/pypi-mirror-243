# Copyright (C) 2023 Cochise Ruhulessin
#
# All rights reserved. No warranty, explicit or implicit, provided. In
# no event shall the author(s) be liable for any claim or damages.
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
from typing import Any
from typing import Protocol
from typing import TypeVar

from .iresourceidentifier import IResourceIdentifier


T = TypeVar('T')


class IStorage(Protocol):
    """The interface for storage classes. A storage class knows how
    to retrieve and persist objects of a specific type.
    """

    async def get(self, key: IResourceIdentifier[Any, T]) -> T | None: ...
    async def persist(self, object: Any) -> None: ...