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
from lusid.models.compliance_parameter import ComplianceParameter
from lusid.models.link import Link
from lusid.models.perpetual_property import PerpetualProperty
from lusid.models.resource_id import ResourceId
from lusid.models.version import Version

class ComplianceRuleResponse(BaseModel):
    """
    ComplianceRuleResponse
    """
    id: Optional[ResourceId] = None
    name: Optional[StrictStr] = None
    description: Optional[StrictStr] = None
    active: Optional[StrictBool] = None
    template_id: Optional[ResourceId] = Field(None, alias="templateId")
    variation: Optional[StrictStr] = None
    portfolio_group_id: Optional[ResourceId] = Field(None, alias="portfolioGroupId")
    parameters: Optional[Dict[str, ComplianceParameter]] = None
    properties: Optional[Dict[str, PerpetualProperty]] = None
    version: Optional[Version] = None
    links: Optional[conlist(Link)] = None
    __properties = ["id", "name", "description", "active", "templateId", "variation", "portfolioGroupId", "parameters", "properties", "version", "links"]

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
    def from_json(cls, json_str: str) -> ComplianceRuleResponse:
        """Create an instance of ComplianceRuleResponse from a JSON string"""
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
        # override the default output from pydantic by calling `to_dict()` of template_id
        if self.template_id:
            _dict['templateId'] = self.template_id.to_dict()
        # override the default output from pydantic by calling `to_dict()` of portfolio_group_id
        if self.portfolio_group_id:
            _dict['portfolioGroupId'] = self.portfolio_group_id.to_dict()
        # override the default output from pydantic by calling `to_dict()` of each value in parameters (dict)
        _field_dict = {}
        if self.parameters:
            for _key in self.parameters:
                if self.parameters[_key]:
                    _field_dict[_key] = self.parameters[_key].to_dict()
            _dict['parameters'] = _field_dict
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
        # set to None if name (nullable) is None
        # and __fields_set__ contains the field
        if self.name is None and "name" in self.__fields_set__:
            _dict['name'] = None

        # set to None if description (nullable) is None
        # and __fields_set__ contains the field
        if self.description is None and "description" in self.__fields_set__:
            _dict['description'] = None

        # set to None if variation (nullable) is None
        # and __fields_set__ contains the field
        if self.variation is None and "variation" in self.__fields_set__:
            _dict['variation'] = None

        # set to None if parameters (nullable) is None
        # and __fields_set__ contains the field
        if self.parameters is None and "parameters" in self.__fields_set__:
            _dict['parameters'] = None

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
    def from_dict(cls, obj: dict) -> ComplianceRuleResponse:
        """Create an instance of ComplianceRuleResponse from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return ComplianceRuleResponse.parse_obj(obj)

        _obj = ComplianceRuleResponse.parse_obj({
            "id": ResourceId.from_dict(obj.get("id")) if obj.get("id") is not None else None,
            "name": obj.get("name"),
            "description": obj.get("description"),
            "active": obj.get("active"),
            "template_id": ResourceId.from_dict(obj.get("templateId")) if obj.get("templateId") is not None else None,
            "variation": obj.get("variation"),
            "portfolio_group_id": ResourceId.from_dict(obj.get("portfolioGroupId")) if obj.get("portfolioGroupId") is not None else None,
            "parameters": dict(
                (_k, ComplianceParameter.from_dict(_v))
                for _k, _v in obj.get("parameters").items()
            )
            if obj.get("parameters") is not None
            else None,
            "properties": dict(
                (_k, PerpetualProperty.from_dict(_v))
                for _k, _v in obj.get("properties").items()
            )
            if obj.get("properties") is not None
            else None,
            "version": Version.from_dict(obj.get("version")) if obj.get("version") is not None else None,
            "links": [Link.from_dict(_item) for _item in obj.get("links")] if obj.get("links") is not None else None
        })
        return _obj
