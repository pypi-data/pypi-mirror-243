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

from datetime import datetime
from typing import Any, Dict, Optional
from pydantic import BaseModel, Field, StrictStr
from lusid.models.resource_id import ResourceId

class ReconciliationSideConfiguration(BaseModel):
    """
    Specification for one side of a valuations/positions scheduled reconciliation  # noqa: E501
    """
    recipe_id: Optional[ResourceId] = Field(None, alias="recipeId")
    effective_at: Optional[datetime] = Field(None, alias="effectiveAt")
    as_at: Optional[datetime] = Field(None, alias="asAt")
    currency: Optional[StrictStr] = None
    __properties = ["recipeId", "effectiveAt", "asAt", "currency"]

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
    def from_json(cls, json_str: str) -> ReconciliationSideConfiguration:
        """Create an instance of ReconciliationSideConfiguration from a JSON string"""
        return cls.from_dict(json.loads(json_str))

    def to_dict(self):
        """Returns the dictionary representation of the model using alias"""
        _dict = self.dict(by_alias=True,
                          exclude={
                          },
                          exclude_none=True)
        # override the default output from pydantic by calling `to_dict()` of recipe_id
        if self.recipe_id:
            _dict['recipeId'] = self.recipe_id.to_dict()
        # set to None if effective_at (nullable) is None
        # and __fields_set__ contains the field
        if self.effective_at is None and "effective_at" in self.__fields_set__:
            _dict['effectiveAt'] = None

        # set to None if as_at (nullable) is None
        # and __fields_set__ contains the field
        if self.as_at is None and "as_at" in self.__fields_set__:
            _dict['asAt'] = None

        # set to None if currency (nullable) is None
        # and __fields_set__ contains the field
        if self.currency is None and "currency" in self.__fields_set__:
            _dict['currency'] = None

        return _dict

    @classmethod
    def from_dict(cls, obj: dict) -> ReconciliationSideConfiguration:
        """Create an instance of ReconciliationSideConfiguration from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return ReconciliationSideConfiguration.parse_obj(obj)

        _obj = ReconciliationSideConfiguration.parse_obj({
            "recipe_id": ResourceId.from_dict(obj.get("recipeId")) if obj.get("recipeId") is not None else None,
            "effective_at": obj.get("effectiveAt"),
            "as_at": obj.get("asAt"),
            "currency": obj.get("currency")
        })
        return _obj
