# coding: utf-8

"""
    LUSID API

    FINBOURNE Technology  # noqa: E501

    Contact: info@finbourne.com
    Generated by OpenAPI Generator (https://openapi-generator.tech)

    Do not edit the class manually.
"""


from __future__ import annotations
import pprint
import re  # noqa: F401
import json

from datetime import datetime
from typing import Any, Dict, Union
from pydantic import BaseModel, Field, StrictFloat, StrictInt

class LevelStep(BaseModel):
    """
    Item which is stepped in level/quantity.  # noqa: E501
    """
    var_date: datetime = Field(..., alias="date", description="The date from which the level should apply.")
    quantity: Union[StrictFloat, StrictInt] = Field(..., description="The quantity which is applied. This might be an absolute, percentage, fractional or other value.")
    __properties = ["date", "quantity"]

    class Config:
        """Pydantic configuration"""
        allow_population_by_field_name = True
        validate_assignment = True

    def to_str(self) -> str:
        """Returns the string representation of the model using alias"""
        return pprint.pformat(self.dict(by_alias=True))

    def to_json(self) -> str:
        """Returns the JSON representation of the model using alias"""
        return json.dumps(self.to_dict())

    @classmethod
    def from_json(cls, json_str: str) -> LevelStep:
        """Create an instance of LevelStep from a JSON string"""
        return cls.from_dict(json.loads(json_str))

    def to_dict(self):
        """Returns the dictionary representation of the model using alias"""
        _dict = self.dict(by_alias=True,
                          exclude={
                          },
                          exclude_none=True)
        return _dict

    @classmethod
    def from_dict(cls, obj: dict) -> LevelStep:
        """Create an instance of LevelStep from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return LevelStep.parse_obj(obj)

        _obj = LevelStep.parse_obj({
            "var_date": obj.get("date"),
            "quantity": obj.get("quantity")
        })
        return _obj
