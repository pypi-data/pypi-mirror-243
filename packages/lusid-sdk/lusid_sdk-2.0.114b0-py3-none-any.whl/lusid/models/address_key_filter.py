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
from pydantic import BaseModel, Field, StrictStr, constr
from lusid.models.result_value import ResultValue

class AddressKeyFilter(BaseModel):
    """
    Class specifying a filtering operation  # noqa: E501
    """
    left: Optional[StrictStr] = Field(None, description="Address for the value in the row")
    operator: Optional[constr(strict=True, max_length=3, min_length=0)] = Field(None, description="What sort of comparison is the filter performing. Can be either \"eq\" for equals or \"neq\" for not equals.")
    right: Optional[ResultValue] = None
    __properties = ["left", "operator", "right"]

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
    def from_json(cls, json_str: str) -> AddressKeyFilter:
        """Create an instance of AddressKeyFilter from a JSON string"""
        return cls.from_dict(json.loads(json_str))

    def to_dict(self):
        """Returns the dictionary representation of the model using alias"""
        _dict = self.dict(by_alias=True,
                          exclude={
                          },
                          exclude_none=True)
        # override the default output from pydantic by calling `to_dict()` of right
        if self.right:
            _dict['right'] = self.right.to_dict()
        # set to None if left (nullable) is None
        # and __fields_set__ contains the field
        if self.left is None and "left" in self.__fields_set__:
            _dict['left'] = None

        # set to None if operator (nullable) is None
        # and __fields_set__ contains the field
        if self.operator is None and "operator" in self.__fields_set__:
            _dict['operator'] = None

        return _dict

    @classmethod
    def from_dict(cls, obj: dict) -> AddressKeyFilter:
        """Create an instance of AddressKeyFilter from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return AddressKeyFilter.parse_obj(obj)

        _obj = AddressKeyFilter.parse_obj({
            "left": obj.get("left"),
            "operator": obj.get("operator"),
            "right": ResultValue.from_dict(obj.get("right")) if obj.get("right") is not None else None
        })
        return _obj
