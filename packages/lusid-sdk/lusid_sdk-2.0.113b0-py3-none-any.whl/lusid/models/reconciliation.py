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
from pydantic import BaseModel, Field, StrictBool, StrictStr, conlist
from lusid.models.link import Link
from lusid.models.model_property import ModelProperty
from lusid.models.reconciliation_configuration import ReconciliationConfiguration
from lusid.models.reconciliation_id import ReconciliationId
from lusid.models.reconciliation_transactions import ReconciliationTransactions
from lusid.models.resource_id import ResourceId
from lusid.models.version import Version

class Reconciliation(BaseModel):
    """
    Representation of Reconciliation in LUSID Api  # noqa: E501
    """
    id: Optional[ReconciliationId] = None
    href: Optional[StrictStr] = Field(None, description="The specific Uniform Resource Identifier (URI) for this resource at the requested effective and asAt datetime.")
    name: Optional[StrictStr] = Field(None, description="The name of the scheduled reconciliation")
    description: Optional[StrictStr] = Field(None, description="A description of the scheduled reconciliation")
    is_portfolio_group: Optional[StrictBool] = Field(None, alias="isPortfolioGroup", description="Specifies whether reconciliation is between portfolios or portfolio groups")
    left: Optional[ResourceId] = None
    right: Optional[ResourceId] = None
    transactions: Optional[ReconciliationTransactions] = None
    positions: Optional[ReconciliationConfiguration] = None
    valuations: Optional[ReconciliationConfiguration] = None
    properties: Optional[Dict[str, ModelProperty]] = Field(None, description="Reconciliation properties")
    version: Optional[Version] = None
    links: Optional[conlist(Link)] = None
    __properties = ["id", "href", "name", "description", "isPortfolioGroup", "left", "right", "transactions", "positions", "valuations", "properties", "version", "links"]

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
    def from_json(cls, json_str: str) -> Reconciliation:
        """Create an instance of Reconciliation from a JSON string"""
        return cls.from_dict(json.loads(json_str))

    def to_dict(self):
        """Returns the dictionary representation of the model using alias"""
        _dict = self.dict(by_alias=True,
                          exclude={
                          },
                          exclude_none=True)
        # override the default output from pydantic by calling `to_dict()` of id
        if self.id:
            _dict['id'] = self.id.to_dict()
        # override the default output from pydantic by calling `to_dict()` of left
        if self.left:
            _dict['left'] = self.left.to_dict()
        # override the default output from pydantic by calling `to_dict()` of right
        if self.right:
            _dict['right'] = self.right.to_dict()
        # override the default output from pydantic by calling `to_dict()` of transactions
        if self.transactions:
            _dict['transactions'] = self.transactions.to_dict()
        # override the default output from pydantic by calling `to_dict()` of positions
        if self.positions:
            _dict['positions'] = self.positions.to_dict()
        # override the default output from pydantic by calling `to_dict()` of valuations
        if self.valuations:
            _dict['valuations'] = self.valuations.to_dict()
        # override the default output from pydantic by calling `to_dict()` of each value in properties (dict)
        _field_dict = {}
        if self.properties:
            for _key in self.properties:
                if self.properties[_key]:
                    _field_dict[_key] = self.properties[_key].to_dict()
            _dict['properties'] = _field_dict
        # override the default output from pydantic by calling `to_dict()` of version
        if self.version:
            _dict['version'] = self.version.to_dict()
        # override the default output from pydantic by calling `to_dict()` of each item in links (list)
        _items = []
        if self.links:
            for _item in self.links:
                if _item:
                    _items.append(_item.to_dict())
            _dict['links'] = _items
        # set to None if href (nullable) is None
        # and __fields_set__ contains the field
        if self.href is None and "href" in self.__fields_set__:
            _dict['href'] = None

        # set to None if name (nullable) is None
        # and __fields_set__ contains the field
        if self.name is None and "name" in self.__fields_set__:
            _dict['name'] = None

        # set to None if description (nullable) is None
        # and __fields_set__ contains the field
        if self.description is None and "description" in self.__fields_set__:
            _dict['description'] = None

        # set to None if properties (nullable) is None
        # and __fields_set__ contains the field
        if self.properties is None and "properties" in self.__fields_set__:
            _dict['properties'] = None

        # set to None if links (nullable) is None
        # and __fields_set__ contains the field
        if self.links is None and "links" in self.__fields_set__:
            _dict['links'] = None

        return _dict

    @classmethod
    def from_dict(cls, obj: dict) -> Reconciliation:
        """Create an instance of Reconciliation from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return Reconciliation.parse_obj(obj)

        _obj = Reconciliation.parse_obj({
            "id": ReconciliationId.from_dict(obj.get("id")) if obj.get("id") is not None else None,
            "href": obj.get("href"),
            "name": obj.get("name"),
            "description": obj.get("description"),
            "is_portfolio_group": obj.get("isPortfolioGroup"),
            "left": ResourceId.from_dict(obj.get("left")) if obj.get("left") is not None else None,
            "right": ResourceId.from_dict(obj.get("right")) if obj.get("right") is not None else None,
            "transactions": ReconciliationTransactions.from_dict(obj.get("transactions")) if obj.get("transactions") is not None else None,
            "positions": ReconciliationConfiguration.from_dict(obj.get("positions")) if obj.get("positions") is not None else None,
            "valuations": ReconciliationConfiguration.from_dict(obj.get("valuations")) if obj.get("valuations") is not None else None,
            "properties": dict(
                (_k, ModelProperty.from_dict(_v))
                for _k, _v in obj.get("properties").items()
            )
            if obj.get("properties") is not None
            else None,
            "version": Version.from_dict(obj.get("version")) if obj.get("version") is not None else None,
            "links": [Link.from_dict(_item) for _item in obj.get("links")] if obj.get("links") is not None else None
        })
        return _obj
