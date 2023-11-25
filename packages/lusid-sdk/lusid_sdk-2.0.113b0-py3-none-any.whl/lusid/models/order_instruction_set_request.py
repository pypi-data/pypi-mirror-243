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
from pydantic import BaseModel, Field, conlist
from lusid.models.order_instruction_request import OrderInstructionRequest

class OrderInstructionSetRequest(BaseModel):
    """
    A request to create or update multiple OrderInstructions.  # noqa: E501
    """
    requests: Optional[conlist(OrderInstructionRequest)] = Field(None, description="A collection of OrderInstructionRequests.")
    __properties = ["requests"]

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
    def from_json(cls, json_str: str) -> OrderInstructionSetRequest:
        """Create an instance of OrderInstructionSetRequest from a JSON string"""
        return cls.from_dict(json.loads(json_str))

    def to_dict(self):
        """Returns the dictionary representation of the model using alias"""
        _dict = self.dict(by_alias=True,
                          exclude={
                          },
                          exclude_none=True)
        # override the default output from pydantic by calling `to_dict()` of each item in requests (list)
        _items = []
        if self.requests:
            for _item in self.requests:
                if _item:
                    _items.append(_item.to_dict())
            _dict['requests'] = _items
        # set to None if requests (nullable) is None
        # and __fields_set__ contains the field
        if self.requests is None and "requests" in self.__fields_set__:
            _dict['requests'] = None

        return _dict

    @classmethod
    def from_dict(cls, obj: dict) -> OrderInstructionSetRequest:
        """Create an instance of OrderInstructionSetRequest from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return OrderInstructionSetRequest.parse_obj(obj)

        _obj = OrderInstructionSetRequest.parse_obj({
            "requests": [OrderInstructionRequest.from_dict(_item) for _item in obj.get("requests")] if obj.get("requests") is not None else None
        })
        return _obj
