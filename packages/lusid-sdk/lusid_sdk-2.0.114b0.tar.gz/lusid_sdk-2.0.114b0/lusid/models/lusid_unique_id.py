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
from pydantic import BaseModel, Field, constr

class LusidUniqueId(BaseModel):
    """
    LusidUniqueId
    """
    type: constr(strict=True, min_length=1) = Field(..., description="The type for the LUSID unique id, this will depend on the type of entity found, for instance 'Instrument' would have a value of 'LusidInstrumentId'")
    value: constr(strict=True, min_length=1) = Field(..., description="The value for the LUSID unique id")
    __properties = ["type", "value"]

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
    def from_json(cls, json_str: str) -> LusidUniqueId:
        """Create an instance of LusidUniqueId from a JSON string"""
        return cls.from_dict(json.loads(json_str))

    def to_dict(self):
        """Returns the dictionary representation of the model using alias"""
        _dict = self.dict(by_alias=True,
                          exclude={
                          },
                          exclude_none=True)
        return _dict

    @classmethod
    def from_dict(cls, obj: dict) -> LusidUniqueId:
        """Create an instance of LusidUniqueId from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return LusidUniqueId.parse_obj(obj)

        _obj = LusidUniqueId.parse_obj({
            "type": obj.get("type"),
            "value": obj.get("value")
        })
        return _obj
