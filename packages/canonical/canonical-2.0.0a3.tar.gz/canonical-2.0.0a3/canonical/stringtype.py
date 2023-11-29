# Copyright (C) 2022 Cochise Ruhulessin
#
# All rights reserved. No warranty, explicit or implicit, provided. In
# no event shall the author(s) be liable for any claim or damages.
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
import re
from typing import Any
from typing import Callable
from typing import Generator


class StringType(str):
    """Base class for string types."""
    __module__: str = 'canonical'
    openapi_title: str | None = None
    openapi_format: str | None = None
    max_length: int | None = None
    min_length: int | None = None
    patterns: re.Pattern[Any] | list[re.Pattern[Any]] = []
    __value: str

    @classmethod
    def __get_pydantic_json_schema__(
        cls,
        field_schema: dict[str, Any]
    ) -> None: # pragma: no cover
        field_schema.update(
            title=cls.openapi_title or cls.__name__,
            type='string'
        )
        if cls.openapi_format:
            field_schema.update(format=cls.openapi_format)

    @classmethod
    def __get_validators__(cls) -> Generator[Callable[..., str | None], None, None]:
        if cls.patterns:
            yield cls.validate_pattern
        yield cls.validate

    @classmethod
    def validate(cls, v: str, _: Any = None) -> str:
        if cls.max_length is not None and len(v) > cls.max_length:
            raise ValueError(f"too long to be a valid {cls.__name__}.")
        if cls.min_length is not None and len(v) < cls.min_length:
            raise ValueError(f"too short to be a valid {cls.__name__}.")
        return v

    @classmethod
    def validate_pattern(cls, v: Any, _: Any = None) -> str:
        if not isinstance(v, str):
            raise ValueError(f"{cls.__name__} must be instantiated from a string type.")
        patterns = cls.patterns
        if not isinstance(patterns, list): # pragma: no cover
            patterns = [patterns]
        for pattern in patterns:
            if not pattern.match(v):
                raise ValueError(f"not a valid {cls.__name__}.")
        return v

    def __repr__(self) -> str: # pragma: no cover
        return f'{type(self).__name__}({self})'