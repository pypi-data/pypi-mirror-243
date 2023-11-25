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
from pydantic import BaseModel, Field
from lusid.models.reconciliation_side_configuration import ReconciliationSideConfiguration
from lusid.models.resource_id import ResourceId

class ReconciliationConfiguration(BaseModel):
    """
    ReconciliationConfiguration
    """
    left: Optional[ReconciliationSideConfiguration] = None
    right: Optional[ReconciliationSideConfiguration] = None
    mapping_id: Optional[ResourceId] = Field(None, alias="mappingId")
    __properties = ["left", "right", "mappingId"]

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
    def from_json(cls, json_str: str) -> ReconciliationConfiguration:
        """Create an instance of ReconciliationConfiguration from a JSON string"""
        return cls.from_dict(json.loads(json_str))

    def to_dict(self):
        """Returns the dictionary representation of the model using alias"""
        _dict = self.dict(by_alias=True,
                          exclude={
                          },
                          exclude_none=True)
        # override the default output from pydantic by calling `to_dict()` of left
        if self.left:
            _dict['left'] = self.left.to_dict()
        # override the default output from pydantic by calling `to_dict()` of right
        if self.right:
            _dict['right'] = self.right.to_dict()
        # override the default output from pydantic by calling `to_dict()` of mapping_id
        if self.mapping_id:
            _dict['mappingId'] = self.mapping_id.to_dict()
        return _dict

    @classmethod
    def from_dict(cls, obj: dict) -> ReconciliationConfiguration:
        """Create an instance of ReconciliationConfiguration from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return ReconciliationConfiguration.parse_obj(obj)

        _obj = ReconciliationConfiguration.parse_obj({
            "left": ReconciliationSideConfiguration.from_dict(obj.get("left")) if obj.get("left") is not None else None,
            "right": ReconciliationSideConfiguration.from_dict(obj.get("right")) if obj.get("right") is not None else None,
            "mapping_id": ResourceId.from_dict(obj.get("mappingId")) if obj.get("mappingId") is not None else None
        })
        return _obj
