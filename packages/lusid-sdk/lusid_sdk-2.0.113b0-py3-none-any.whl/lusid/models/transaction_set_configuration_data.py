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
from lusid.models.link import Link
from lusid.models.side_configuration_data import SideConfigurationData
from lusid.models.transaction_configuration_data import TransactionConfigurationData

class TransactionSetConfigurationData(BaseModel):
    """
    A collection of the data required to configure transaction types..  # noqa: E501
    """
    transaction_configs: conlist(TransactionConfigurationData) = Field(..., alias="transactionConfigs", description="Collection of transaction type models")
    side_definitions: Optional[conlist(SideConfigurationData)] = Field(None, alias="sideDefinitions", description="Collection of side definitions")
    links: Optional[conlist(Link)] = None
    __properties = ["transactionConfigs", "sideDefinitions", "links"]

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
    def from_json(cls, json_str: str) -> TransactionSetConfigurationData:
        """Create an instance of TransactionSetConfigurationData from a JSON string"""
        return cls.from_dict(json.loads(json_str))

    def to_dict(self):
        """Returns the dictionary representation of the model using alias"""
        _dict = self.dict(by_alias=True,
                          exclude={
                          },
                          exclude_none=True)
        # override the default output from pydantic by calling `to_dict()` of each item in transaction_configs (list)
        _items = []
        if self.transaction_configs:
            for _item in self.transaction_configs:
                if _item:
                    _items.append(_item.to_dict())
            _dict['transactionConfigs'] = _items
        # override the default output from pydantic by calling `to_dict()` of each item in side_definitions (list)
        _items = []
        if self.side_definitions:
            for _item in self.side_definitions:
                if _item:
                    _items.append(_item.to_dict())
            _dict['sideDefinitions'] = _items
        # override the default output from pydantic by calling `to_dict()` of each item in links (list)
        _items = []
        if self.links:
            for _item in self.links:
                if _item:
                    _items.append(_item.to_dict())
            _dict['links'] = _items
        # set to None if side_definitions (nullable) is None
        # and __fields_set__ contains the field
        if self.side_definitions is None and "side_definitions" in self.__fields_set__:
            _dict['sideDefinitions'] = None

        # set to None if links (nullable) is None
        # and __fields_set__ contains the field
        if self.links is None and "links" in self.__fields_set__:
            _dict['links'] = None

        return _dict

    @classmethod
    def from_dict(cls, obj: dict) -> TransactionSetConfigurationData:
        """Create an instance of TransactionSetConfigurationData from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return TransactionSetConfigurationData.parse_obj(obj)

        _obj = TransactionSetConfigurationData.parse_obj({
            "transaction_configs": [TransactionConfigurationData.from_dict(_item) for _item in obj.get("transactionConfigs")] if obj.get("transactionConfigs") is not None else None,
            "side_definitions": [SideConfigurationData.from_dict(_item) for _item in obj.get("sideDefinitions")] if obj.get("sideDefinitions") is not None else None,
            "links": [Link.from_dict(_item) for _item in obj.get("links")] if obj.get("links") is not None else None
        })
        return _obj
