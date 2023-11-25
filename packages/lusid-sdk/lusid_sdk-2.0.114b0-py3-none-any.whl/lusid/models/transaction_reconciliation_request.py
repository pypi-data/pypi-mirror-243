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
from lusid.models.resource_id import ResourceId

class TransactionReconciliationRequest(BaseModel):
    """
    Specifies the parameter to be use when performing a Transaction Reconciliation.  # noqa: E501
    """
    left_portfolio_id: ResourceId = Field(..., alias="leftPortfolioId")
    right_portfolio_id: ResourceId = Field(..., alias="rightPortfolioId")
    mapping_id: Optional[ResourceId] = Field(None, alias="mappingId")
    from_transaction_date: datetime = Field(..., alias="fromTransactionDate")
    to_transaction_date: datetime = Field(..., alias="toTransactionDate")
    as_at: Optional[datetime] = Field(None, alias="asAt")
    property_keys: Optional[conlist(StrictStr)] = Field(None, alias="propertyKeys")
    __properties = ["leftPortfolioId", "rightPortfolioId", "mappingId", "fromTransactionDate", "toTransactionDate", "asAt", "propertyKeys"]

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
    def from_json(cls, json_str: str) -> TransactionReconciliationRequest:
        """Create an instance of TransactionReconciliationRequest from a JSON string"""
        return cls.from_dict(json.loads(json_str))

    def to_dict(self):
        """Returns the dictionary representation of the model using alias"""
        _dict = self.dict(by_alias=True,
                          exclude={
                          },
                          exclude_none=True)
        # override the default output from pydantic by calling `to_dict()` of left_portfolio_id
        if self.left_portfolio_id:
            _dict['leftPortfolioId'] = self.left_portfolio_id.to_dict()
        # override the default output from pydantic by calling `to_dict()` of right_portfolio_id
        if self.right_portfolio_id:
            _dict['rightPortfolioId'] = self.right_portfolio_id.to_dict()
        # override the default output from pydantic by calling `to_dict()` of mapping_id
        if self.mapping_id:
            _dict['mappingId'] = self.mapping_id.to_dict()
        # set to None if as_at (nullable) is None
        # and __fields_set__ contains the field
        if self.as_at is None and "as_at" in self.__fields_set__:
            _dict['asAt'] = None

        # set to None if property_keys (nullable) is None
        # and __fields_set__ contains the field
        if self.property_keys is None and "property_keys" in self.__fields_set__:
            _dict['propertyKeys'] = None

        return _dict

    @classmethod
    def from_dict(cls, obj: dict) -> TransactionReconciliationRequest:
        """Create an instance of TransactionReconciliationRequest from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return TransactionReconciliationRequest.parse_obj(obj)

        _obj = TransactionReconciliationRequest.parse_obj({
            "left_portfolio_id": ResourceId.from_dict(obj.get("leftPortfolioId")) if obj.get("leftPortfolioId") is not None else None,
            "right_portfolio_id": ResourceId.from_dict(obj.get("rightPortfolioId")) if obj.get("rightPortfolioId") is not None else None,
            "mapping_id": ResourceId.from_dict(obj.get("mappingId")) if obj.get("mappingId") is not None else None,
            "from_transaction_date": obj.get("fromTransactionDate"),
            "to_transaction_date": obj.get("toTransactionDate"),
            "as_at": obj.get("asAt"),
            "property_keys": obj.get("propertyKeys")
        })
        return _obj
