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


from typing import Any, Dict, Optional
from pydantic import BaseModel, Field, constr

class DialectSchema(BaseModel):
    """
    A schema that a given document must obey. A representation of the validation of a particular Dialect,  in a given language.  # noqa: E501
    """
    type: constr(strict=True, min_length=1) = Field(..., description="The type of schema this represents")
    body: Optional[constr(strict=True, max_length=128000, min_length=0)] = Field(None, description="The body of the schema")
    __properties = ["type", "body"]

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
    def from_json(cls, json_str: str) -> DialectSchema:
        """Create an instance of DialectSchema from a JSON string"""
        return cls.from_dict(json.loads(json_str))

    def to_dict(self):
        """Returns the dictionary representation of the model using alias"""
        _dict = self.dict(by_alias=True,
                          exclude={
                          },
                          exclude_none=True)
        # set to None if body (nullable) is None
        # and __fields_set__ contains the field
        if self.body is None and "body" in self.__fields_set__:
            _dict['body'] = None

        return _dict

    @classmethod
    def from_dict(cls, obj: dict) -> DialectSchema:
        """Create an instance of DialectSchema from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return DialectSchema.parse_obj(obj)

        _obj = DialectSchema.parse_obj({
            "type": obj.get("type"),
            "body": obj.get("body")
        })
        return _obj
