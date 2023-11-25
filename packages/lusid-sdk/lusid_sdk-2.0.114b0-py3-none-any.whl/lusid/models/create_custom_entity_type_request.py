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


from typing import Any, Dict, List
from pydantic import BaseModel, Field, conlist, constr, validator
from lusid.models.custom_entity_field_definition import CustomEntityFieldDefinition

class CreateCustomEntityTypeRequest(BaseModel):
    """
    CreateCustomEntityTypeRequest
    """
    entity_type_name: constr(strict=True, max_length=64, min_length=1) = Field(..., alias="entityTypeName", description="A name for the custom entity type. This will be prefixed with “~” and returned as “entityType”, which is the identifier for the custom entity type.")
    display_name: constr(strict=True, min_length=1) = Field(..., alias="displayName", description="A display label for the custom entity type.")
    description: constr(strict=True, min_length=1) = Field(..., description="A description for the custom entity type.")
    field_schema: conlist(CustomEntityFieldDefinition) = Field(..., alias="fieldSchema", description="The description of the fields on the custom entity type.")
    __properties = ["entityTypeName", "displayName", "description", "fieldSchema"]

    @validator('display_name')
    def display_name_validate_regular_expression(cls, value):
        """Validates the regular expression"""
        if not re.match(r"^[\s\S]*$", value):
            raise ValueError(r"must validate the regular expression /^[\s\S]*$/")
        return value

    @validator('description')
    def description_validate_regular_expression(cls, value):
        """Validates the regular expression"""
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
    def from_json(cls, json_str: str) -> CreateCustomEntityTypeRequest:
        """Create an instance of CreateCustomEntityTypeRequest from a JSON string"""
        return cls.from_dict(json.loads(json_str))

    def to_dict(self):
        """Returns the dictionary representation of the model using alias"""
        _dict = self.dict(by_alias=True,
                          exclude={
                          },
                          exclude_none=True)
        # override the default output from pydantic by calling `to_dict()` of each item in field_schema (list)
        _items = []
        if self.field_schema:
            for _item in self.field_schema:
                if _item:
                    _items.append(_item.to_dict())
            _dict['fieldSchema'] = _items
        return _dict

    @classmethod
    def from_dict(cls, obj: dict) -> CreateCustomEntityTypeRequest:
        """Create an instance of CreateCustomEntityTypeRequest from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return CreateCustomEntityTypeRequest.parse_obj(obj)

        _obj = CreateCustomEntityTypeRequest.parse_obj({
            "entity_type_name": obj.get("entityTypeName"),
            "display_name": obj.get("displayName"),
            "description": obj.get("description"),
            "field_schema": [CustomEntityFieldDefinition.from_dict(_item) for _item in obj.get("fieldSchema")] if obj.get("fieldSchema") is not None else None
        })
        return _obj
