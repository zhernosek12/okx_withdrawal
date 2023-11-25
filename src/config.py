import random
from pathlib import Path
from typing import Any, Dict, List, Optional, Union

import yaml
from pydantic import BaseModel, field_validator
from pydantic_core.core_schema import ValidationInfo


class RangeFloat(BaseModel):
    from_value: float
    to_value: float

    @property
    def value(self) -> float:
        return round(random.uniform(self.from_value, self.to_value), random.randint(7, 11))


class RangeInt(BaseModel):
    from_value: int
    to_value: int

    @property
    def value(self) -> int:
        return random.randint(self.from_value, self.to_value)


def update_range_fields(cls, value: List[Union[int, float]], info: ValidationInfo) -> Any:
    if value and isinstance(value[0], int):
        value = RangeInt(from_value=value[0], to_value=value[1])
    elif value and isinstance(value[0], float):
        value = RangeFloat(from_value=value[0], to_value=value[1])
    return value


class AppConfig(BaseModel):
    @field_validator("amount_withdraw", "sleep_after_withdraw", mode="before")
    def update_range_fields(cls, value: Any, info: ValidationInfo) -> Any:
        return update_range_fields(cls, value, info)

    okx_key: str
    okx_secret: str
    okx_password: str
    shuffle: bool
    symbol: str
    network: str
    amount_withdraw: RangeFloat
    sleep_after_withdraw: RangeInt


_config_path = Path(__file__).resolve().parent.parent / "config.yaml"
with _config_path.open(encoding="utf-8") as f:
    _data = yaml.safe_load(f)

config = AppConfig.model_validate(_data)
