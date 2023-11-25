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
from pydantic import BaseModel, Field, StrictStr, conlist
from lusid.models.model_property import ModelProperty
from lusid.models.relationship import Relationship
from lusid.models.version import Version

class Person(BaseModel):
    """
    Person
    """
    display_name: Optional[StrictStr] = Field(None, alias="displayName", description="The display name of the Person")
    description: Optional[StrictStr] = Field(None, description="The description of the Person")
    href: Optional[StrictStr] = Field(None, description="The specifc Uniform Resource Identifier (URI) for this resource at the requested effective and asAt datetime.")
    lusid_person_id: Optional[StrictStr] = Field(None, alias="lusidPersonId", description="The unique LUSID Person Identifier of the Person.")
    identifiers: Optional[Dict[str, ModelProperty]] = Field(None, description="Unique client-defined identifiers of the Person.")
    properties: Optional[Dict[str, ModelProperty]] = Field(None, description="A set of properties associated to the Person. There can be multiple properties associated with a property key.")
    relationships: Optional[conlist(Relationship)] = Field(None, description="A set of relationships associated to the Person.")
    version: Optional[Version] = None
    __properties = ["displayName", "description", "href", "lusidPersonId", "identifiers", "properties", "relationships", "version"]

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
    def from_json(cls, json_str: str) -> Person:
        """Create an instance of Person from a JSON string"""
        return cls.from_dict(json.loads(json_str))

    def to_dict(self):
        """Returns the dictionary representation of the model using alias"""
        _dict = self.dict(by_alias=True,
                          exclude={
                          },
                          exclude_none=True)
        # override the default output from pydantic by calling `to_dict()` of each value in identifiers (dict)
        _field_dict = {}
        if self.identifiers:
            for _key in self.identifiers:
                if self.identifiers[_key]:
                    _field_dict[_key] = self.identifiers[_key].to_dict()
            _dict['identifiers'] = _field_dict
        # override the default output from pydantic by calling `to_dict()` of each value in properties (dict)
        _field_dict = {}
        if self.properties:
            for _key in self.properties:
                if self.properties[_key]:
                    _field_dict[_key] = self.properties[_key].to_dict()
            _dict['properties'] = _field_dict
        # override the default output from pydantic by calling `to_dict()` of each item in relationships (list)
        _items = []
        if self.relationships:
            for _item in self.relationships:
                if _item:
                    _items.append(_item.to_dict())
            _dict['relationships'] = _items
        # override the default output from pydantic by calling `to_dict()` of version
        if self.version:
            _dict['version'] = self.version.to_dict()
        # set to None if display_name (nullable) is None
        # and __fields_set__ contains the field
        if self.display_name is None and "display_name" in self.__fields_set__:
            _dict['displayName'] = None

        # set to None if description (nullable) is None
        # and __fields_set__ contains the field
        if self.description is None and "description" in self.__fields_set__:
            _dict['description'] = None

        # set to None if href (nullable) is None
        # and __fields_set__ contains the field
        if self.href is None and "href" in self.__fields_set__:
            _dict['href'] = None

        # set to None if lusid_person_id (nullable) is None
        # and __fields_set__ contains the field
        if self.lusid_person_id is None and "lusid_person_id" in self.__fields_set__:
            _dict['lusidPersonId'] = None

        # set to None if identifiers (nullable) is None
        # and __fields_set__ contains the field
        if self.identifiers is None and "identifiers" in self.__fields_set__:
            _dict['identifiers'] = None

        # set to None if properties (nullable) is None
        # and __fields_set__ contains the field
        if self.properties is None and "properties" in self.__fields_set__:
            _dict['properties'] = None

        # set to None if relationships (nullable) is None
        # and __fields_set__ contains the field
        if self.relationships is None and "relationships" in self.__fields_set__:
            _dict['relationships'] = None

        return _dict

    @classmethod
    def from_dict(cls, obj: dict) -> Person:
        """Create an instance of Person from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return Person.parse_obj(obj)

        _obj = Person.parse_obj({
            "display_name": obj.get("displayName"),
            "description": obj.get("description"),
            "href": obj.get("href"),
            "lusid_person_id": obj.get("lusidPersonId"),
            "identifiers": dict(
                (_k, ModelProperty.from_dict(_v))
                for _k, _v in obj.get("identifiers").items()
            )
            if obj.get("identifiers") is not None
            else None,
            "properties": dict(
                (_k, ModelProperty.from_dict(_v))
                for _k, _v in obj.get("properties").items()
            )
            if obj.get("properties") is not None
            else None,
            "relationships": [Relationship.from_dict(_item) for _item in obj.get("relationships")] if obj.get("relationships") is not None else None,
            "version": Version.from_dict(obj.get("version")) if obj.get("version") is not None else None
        })
        return _obj
