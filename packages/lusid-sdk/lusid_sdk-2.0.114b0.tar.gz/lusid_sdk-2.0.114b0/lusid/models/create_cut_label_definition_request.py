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
from pydantic import BaseModel, Field, StrictStr, constr, validator
from lusid.models.cut_local_time import CutLocalTime

class CreateCutLabelDefinitionRequest(BaseModel):
    """
    This request specifies a new Cut Label Definition  # noqa: E501
    """
    code: StrictStr = Field(...)
    display_name: constr(strict=True, min_length=1) = Field(..., alias="displayName")
    description: Optional[constr(strict=True)] = None
    cut_local_time: CutLocalTime = Field(..., alias="cutLocalTime")
    time_zone: constr(strict=True, min_length=1) = Field(..., alias="timeZone")
    __properties = ["code", "displayName", "description", "cutLocalTime", "timeZone"]

    @validator('display_name')
    def display_name_validate_regular_expression(cls, value):
        """Validates the regular expression"""
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
    def from_json(cls, json_str: str) -> CreateCutLabelDefinitionRequest:
        """Create an instance of CreateCutLabelDefinitionRequest from a JSON string"""
        return cls.from_dict(json.loads(json_str))

    def to_dict(self):
        """Returns the dictionary representation of the model using alias"""
        _dict = self.dict(by_alias=True,
                          exclude={
                          },
                          exclude_none=True)
        # override the default output from pydantic by calling `to_dict()` of cut_local_time
        if self.cut_local_time:
            _dict['cutLocalTime'] = self.cut_local_time.to_dict()
        # set to None if description (nullable) is None
        # and __fields_set__ contains the field
        if self.description is None and "description" in self.__fields_set__:
            _dict['description'] = None

        return _dict

    @classmethod
    def from_dict(cls, obj: dict) -> CreateCutLabelDefinitionRequest:
        """Create an instance of CreateCutLabelDefinitionRequest from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return CreateCutLabelDefinitionRequest.parse_obj(obj)

        _obj = CreateCutLabelDefinitionRequest.parse_obj({
            "code": obj.get("code"),
            "display_name": obj.get("displayName"),
            "description": obj.get("description"),
            "cut_local_time": CutLocalTime.from_dict(obj.get("cutLocalTime")) if obj.get("cutLocalTime") is not None else None,
            "time_zone": obj.get("timeZone")
        })
        return _obj
