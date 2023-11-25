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


from typing import Any, Dict
from pydantic import BaseModel, Field, StrictStr, validator

class OrderBySpec(BaseModel):
    """
    OrderBySpec
    """
    key: StrictStr = Field(..., description="The key that uniquely identifies a queryable address in Lusid.")
    sort_order: StrictStr = Field(..., alias="sortOrder", description="The available values are: Ascending, Descending")
    __properties = ["key", "sortOrder"]

    @validator('sort_order')
    def sort_order_validate_enum(cls, value):
        """Validates the enum"""
        if value not in ('Ascending', 'Descending'):
            raise ValueError("must be one of enum values ('Ascending', 'Descending')")
        return value

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
    def from_json(cls, json_str: str) -> OrderBySpec:
        """Create an instance of OrderBySpec from a JSON string"""
        return cls.from_dict(json.loads(json_str))

    def to_dict(self):
        """Returns the dictionary representation of the model using alias"""
        _dict = self.dict(by_alias=True,
                          exclude={
                          },
                          exclude_none=True)
        return _dict

    @classmethod
    def from_dict(cls, obj: dict) -> OrderBySpec:
        """Create an instance of OrderBySpec from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return OrderBySpec.parse_obj(obj)

        _obj = OrderBySpec.parse_obj({
            "key": obj.get("key"),
            "sort_order": obj.get("sortOrder")
        })
        return _obj
