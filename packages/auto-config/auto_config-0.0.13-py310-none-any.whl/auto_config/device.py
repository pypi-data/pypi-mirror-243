from __future__ import annotations

from pydantic import BaseModel, Field

from .field import BaseExtraField
from typing import Generic, TypeVar

__Device_ExtraT = TypeVar("__Device_ExtraT", bound = BaseExtraField)


class Device(BaseModel, Generic[__Device_ExtraT]):
    system: str
    hardware: str
    group: str
    main: bool = False
    desc: str = Field("")

    extra: __Device_ExtraT = Field(default_factory=BaseExtraField)

    def get_name(self):
        return f"{self.group}-{self.hardware}-{self.system}"

    def get_domain(self):
        return f"{self.hardware}-{self.system}.ssh.{self.group}"
