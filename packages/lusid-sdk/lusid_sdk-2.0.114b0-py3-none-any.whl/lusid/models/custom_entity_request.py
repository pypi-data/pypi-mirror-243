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
from pydantic import BaseModel, Field, conlist, constr
from lusid.models.custom_entity_field import CustomEntityField
from lusid.models.custom_entity_id import CustomEntityId

class CustomEntityRequest(BaseModel):
    """
    CustomEntityRequest
    """
    display_name: constr(strict=True, min_length=1) = Field(..., alias="displayName", description="A display label for the custom entity.")
    description: constr(strict=True, min_length=1) = Field(..., description="A description of the custom entity.")
    identifiers: conlist(CustomEntityId) = Field(..., description="The identifiers the custom entity will be upserted with.")
    fields: Optional[conlist(CustomEntityField)] = Field(None, description="The fields that decorate the custom entity.")
    __properties = ["displayName", "description", "identifiers", "fields"]

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
    def from_json(cls, json_str: str) -> CustomEntityRequest:
        """Create an instance of CustomEntityRequest from a JSON string"""
        return cls.from_dict(json.loads(json_str))

    def to_dict(self):
        """Returns the dictionary representation of the model using alias"""
        _dict = self.dict(by_alias=True,
                          exclude={
                          },
                          exclude_none=True)
        # override the default output from pydantic by calling `to_dict()` of each item in identifiers (list)
        _items = []
        if self.identifiers:
            for _item in self.identifiers:
                if _item:
                    _items.append(_item.to_dict())
            _dict['identifiers'] = _items
        # override the default output from pydantic by calling `to_dict()` of each item in fields (list)
        _items = []
        if self.fields:
            for _item in self.fields:
                if _item:
                    _items.append(_item.to_dict())
            _dict['fields'] = _items
        # set to None if fields (nullable) is None
        # and __fields_set__ contains the field
        if self.fields is None and "fields" in self.__fields_set__:
            _dict['fields'] = None

        return _dict

    @classmethod
    def from_dict(cls, obj: dict) -> CustomEntityRequest:
        """Create an instance of CustomEntityRequest from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return CustomEntityRequest.parse_obj(obj)

        _obj = CustomEntityRequest.parse_obj({
            "display_name": obj.get("displayName"),
            "description": obj.get("description"),
            "identifiers": [CustomEntityId.from_dict(_item) for _item in obj.get("identifiers")] if obj.get("identifiers") is not None else None,
            "fields": [CustomEntityField.from_dict(_item) for _item in obj.get("fields")] if obj.get("fields") is not None else None
        })
        return _obj
