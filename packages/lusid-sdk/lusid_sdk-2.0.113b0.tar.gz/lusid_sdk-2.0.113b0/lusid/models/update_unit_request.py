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
from pydantic import BaseModel, Field, constr, validator

class UpdateUnitRequest(BaseModel):
    """
    UpdateUnitRequest
    """
    code: Optional[constr(strict=True, max_length=64, min_length=1)] = None
    display_name: Optional[constr(strict=True, max_length=512, min_length=1)] = Field(None, alias="displayName")
    description: Optional[constr(strict=True, max_length=512, min_length=1)] = None
    __properties = ["code", "displayName", "description"]

    @validator('code')
    def code_validate_regular_expression(cls, value):
        """Validates the regular expression"""
        if value is None:
            return value

        if not re.match(r"^[a-zA-Z0-9\-_]+$", value):
            raise ValueError(r"must validate the regular expression /^[a-zA-Z0-9\-_]+$/")
        return value

    @validator('display_name')
    def display_name_validate_regular_expression(cls, value):
        """Validates the regular expression"""
        if value is None:
            return value

        if not re.match(r"^[\s\S]*$", value):
            raise ValueError(r"must validate the regular expression /^[\s\S]*$/")
        return value

    @validator('description')
    def description_validate_regular_expression(cls, value):
        """Validates the regular expression"""
        if value is None:
            return value

        if not re.match(r"^[\s\S]*$", value):
            raise ValueError(r"must validate the regular expression /^[\s\S]*$/")
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
    def from_json(cls, json_str: str) -> UpdateUnitRequest:
        """Create an instance of UpdateUnitRequest from a JSON string"""
        return cls.from_dict(json.loads(json_str))

    def to_dict(self):
        """Returns the dictionary representation of the model using alias"""
        _dict = self.dict(by_alias=True,
                          exclude={
                          },
                          exclude_none=True)
        # set to None if code (nullable) is None
        # and __fields_set__ contains the field
        if self.code is None and "code" in self.__fields_set__:
            _dict['code'] = None

        # set to None if display_name (nullable) is None
        # and __fields_set__ contains the field
        if self.display_name is None and "display_name" in self.__fields_set__:
            _dict['displayName'] = None

        # set to None if description (nullable) is None
        # and __fields_set__ contains the field
        if self.description is None and "description" in self.__fields_set__:
            _dict['description'] = None

        return _dict

    @classmethod
    def from_dict(cls, obj: dict) -> UpdateUnitRequest:
        """Create an instance of UpdateUnitRequest from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return UpdateUnitRequest.parse_obj(obj)

        _obj = UpdateUnitRequest.parse_obj({
            "code": obj.get("code"),
            "display_name": obj.get("displayName"),
            "description": obj.get("description")
        })
        return _obj
