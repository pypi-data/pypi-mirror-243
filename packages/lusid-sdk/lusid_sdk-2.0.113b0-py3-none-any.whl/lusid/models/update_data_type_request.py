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


from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field, StrictStr, conlist, constr, validator
from lusid.models.update_unit_request import UpdateUnitRequest

class UpdateDataTypeRequest(BaseModel):
    """
    UpdateDataTypeRequest
    """
    display_name: Optional[constr(strict=True, max_length=512, min_length=1)] = Field(None, alias="displayName", description="The display name of the data type.")
    description: Optional[constr(strict=True, max_length=1024, min_length=0)] = Field(None, description="The description of the data type.")
    acceptable_values: Optional[conlist(StrictStr)] = Field(None, alias="acceptableValues", description="The acceptable set of values for this data type. Only applies to 'open' value type range.")
    acceptable_units: Optional[conlist(UpdateUnitRequest)] = Field(None, alias="acceptableUnits", description="The definitions of the acceptable units.")
    __properties = ["displayName", "description", "acceptableValues", "acceptableUnits"]

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
    def from_json(cls, json_str: str) -> UpdateDataTypeRequest:
        """Create an instance of UpdateDataTypeRequest from a JSON string"""
        return cls.from_dict(json.loads(json_str))

    def to_dict(self):
        """Returns the dictionary representation of the model using alias"""
        _dict = self.dict(by_alias=True,
                          exclude={
                          },
                          exclude_none=True)
        # override the default output from pydantic by calling `to_dict()` of each item in acceptable_units (list)
        _items = []
        if self.acceptable_units:
            for _item in self.acceptable_units:
                if _item:
                    _items.append(_item.to_dict())
            _dict['acceptableUnits'] = _items
        # set to None if display_name (nullable) is None
        # and __fields_set__ contains the field
        if self.display_name is None and "display_name" in self.__fields_set__:
            _dict['displayName'] = None

        # set to None if description (nullable) is None
        # and __fields_set__ contains the field
        if self.description is None and "description" in self.__fields_set__:
            _dict['description'] = None

        # set to None if acceptable_values (nullable) is None
        # and __fields_set__ contains the field
        if self.acceptable_values is None and "acceptable_values" in self.__fields_set__:
            _dict['acceptableValues'] = None

        # set to None if acceptable_units (nullable) is None
        # and __fields_set__ contains the field
        if self.acceptable_units is None and "acceptable_units" in self.__fields_set__:
            _dict['acceptableUnits'] = None

        return _dict

    @classmethod
    def from_dict(cls, obj: dict) -> UpdateDataTypeRequest:
        """Create an instance of UpdateDataTypeRequest from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return UpdateDataTypeRequest.parse_obj(obj)

        _obj = UpdateDataTypeRequest.parse_obj({
            "display_name": obj.get("displayName"),
            "description": obj.get("description"),
            "acceptable_values": obj.get("acceptableValues"),
            "acceptable_units": [UpdateUnitRequest.from_dict(_item) for _item in obj.get("acceptableUnits")] if obj.get("acceptableUnits") is not None else None
        })
        return _obj
