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
from lusid.models.error_detail import ErrorDetail
from lusid.models.link import Link
from lusid.models.response_meta_data import ResponseMetaData
from lusid.models.transaction import Transaction

class BatchUpsertPortfolioTransactionsResponse(BaseModel):
    """
    BatchUpsertPortfolioTransactionsResponse
    """
    values: Optional[Dict[str, Transaction]] = Field(None, description="The transactions which have been successfully upserted.")
    failed: Optional[Dict[str, ErrorDetail]] = Field(None, description="The transactions that could not be upserted along with a reason for their failure.")
    metadata: Optional[Dict[str, conlist(ResponseMetaData)]] = Field(None, description="Contains warnings related to unresolved instruments or non-existent transaction types for the upserted trades")
    links: Optional[conlist(Link)] = None
    __properties = ["values", "failed", "metadata", "links"]

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
    def from_json(cls, json_str: str) -> BatchUpsertPortfolioTransactionsResponse:
        """Create an instance of BatchUpsertPortfolioTransactionsResponse from a JSON string"""
        return cls.from_dict(json.loads(json_str))

    def to_dict(self):
        """Returns the dictionary representation of the model using alias"""
        _dict = self.dict(by_alias=True,
                          exclude={
                          },
                          exclude_none=True)
        # override the default output from pydantic by calling `to_dict()` of each value in values (dict)
        _field_dict = {}
        if self.values:
            for _key in self.values:
                if self.values[_key]:
                    _field_dict[_key] = self.values[_key].to_dict()
            _dict['values'] = _field_dict
        # override the default output from pydantic by calling `to_dict()` of each value in failed (dict)
        _field_dict = {}
        if self.failed:
            for _key in self.failed:
                if self.failed[_key]:
                    _field_dict[_key] = self.failed[_key].to_dict()
            _dict['failed'] = _field_dict
        # override the default output from pydantic by calling `to_dict()` of each value in metadata (dict of array)
        _field_dict_of_array = {}
        if self.metadata:
            for _key in self.metadata:
                if self.metadata[_key]:
                    _field_dict_of_array[_key] = [
                        _item.to_dict() for _item in self.metadata[_key]
                    ]
            _dict['metadata'] = _field_dict_of_array
        # override the default output from pydantic by calling `to_dict()` of each item in links (list)
        _items = []
        if self.links:
            for _item in self.links:
                if _item:
                    _items.append(_item.to_dict())
            _dict['links'] = _items
        # set to None if values (nullable) is None
        # and __fields_set__ contains the field
        if self.values is None and "values" in self.__fields_set__:
            _dict['values'] = None

        # set to None if failed (nullable) is None
        # and __fields_set__ contains the field
        if self.failed is None and "failed" in self.__fields_set__:
            _dict['failed'] = None

        # set to None if metadata (nullable) is None
        # and __fields_set__ contains the field
        if self.metadata is None and "metadata" in self.__fields_set__:
            _dict['metadata'] = None

        # set to None if links (nullable) is None
        # and __fields_set__ contains the field
        if self.links is None and "links" in self.__fields_set__:
            _dict['links'] = None

        return _dict

    @classmethod
    def from_dict(cls, obj: dict) -> BatchUpsertPortfolioTransactionsResponse:
        """Create an instance of BatchUpsertPortfolioTransactionsResponse from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return BatchUpsertPortfolioTransactionsResponse.parse_obj(obj)

        _obj = BatchUpsertPortfolioTransactionsResponse.parse_obj({
            "values": dict(
                (_k, Transaction.from_dict(_v))
                for _k, _v in obj.get("values").items()
            )
            if obj.get("values") is not None
            else None,
            "failed": dict(
                (_k, ErrorDetail.from_dict(_v))
                for _k, _v in obj.get("failed").items()
            )
            if obj.get("failed") is not None
            else None,
            "metadata": dict(
                (_k,
                        [ResponseMetaData.from_dict(_item) for _item in _v]
                        if _v is not None
                        else None
                )
                for _k, _v in obj.get("metadata").items()
            ),
            "links": [Link.from_dict(_item) for _item in obj.get("links")] if obj.get("links") is not None else None
        })
        return _obj
