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
from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field, StrictStr, conlist
from lusid.models.error_detail import ErrorDetail
from lusid.models.link import Link
from lusid.models.version import Version

class UpsertReturnsResponse(BaseModel):
    """
    Response from upserting Returns  # noqa: E501
    """
    version: Version = Field(...)
    href: Optional[StrictStr] = Field(None, description="The specific Uniform Resource Identifier (URI) for this resource at the requested effective and asAt datetime.")
    values: Optional[conlist(Dict[str, datetime])] = Field(None, description="The set of values that were successfully retrieved.")
    failed: Optional[conlist(Dict[str, ErrorDetail])] = Field(None, description="The set of values that could not be retrieved due along with a reason for this, e.g badly formed request.")
    links: Optional[conlist(Link)] = None
    __properties = ["version", "href", "values", "failed", "links"]

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
    def from_json(cls, json_str: str) -> UpsertReturnsResponse:
        """Create an instance of UpsertReturnsResponse from a JSON string"""
        return cls.from_dict(json.loads(json_str))

    def to_dict(self):
        """Returns the dictionary representation of the model using alias"""
        _dict = self.dict(by_alias=True,
                          exclude={
                          },
                          exclude_none=True)
        # override the default output from pydantic by calling `to_dict()` of version
        if self.version:
            _dict['version'] = self.version.to_dict()
        # override the default output from pydantic by calling `to_dict()` of each item in failed (list)
        _items = []
        if self.failed:
            for _item in self.failed:
                if _item:
                    _items.append(_item.to_dict())
            _dict['failed'] = _items
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

        # set to None if values (nullable) is None
        # and __fields_set__ contains the field
        if self.values is None and "values" in self.__fields_set__:
            _dict['values'] = None

        # set to None if failed (nullable) is None
        # and __fields_set__ contains the field
        if self.failed is None and "failed" in self.__fields_set__:
            _dict['failed'] = None

        # set to None if links (nullable) is None
        # and __fields_set__ contains the field
        if self.links is None and "links" in self.__fields_set__:
            _dict['links'] = None

        return _dict

    @classmethod
    def from_dict(cls, obj: dict) -> UpsertReturnsResponse:
        """Create an instance of UpsertReturnsResponse from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return UpsertReturnsResponse.parse_obj(obj)

        _obj = UpsertReturnsResponse.parse_obj({
            "version": Version.from_dict(obj.get("version")) if obj.get("version") is not None else None,
            "href": obj.get("href"),
            "values": obj.get("values"),
            "failed": [Dict[str, ErrorDetail].from_dict(_item) for _item in obj.get("failed")] if obj.get("failed") is not None else None,
            "links": [Link.from_dict(_item) for _item in obj.get("links")] if obj.get("links") is not None else None
        })
        return _obj
