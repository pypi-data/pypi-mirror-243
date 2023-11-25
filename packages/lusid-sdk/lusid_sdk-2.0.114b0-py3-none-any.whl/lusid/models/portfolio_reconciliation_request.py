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
from pydantic import BaseModel, Field, constr
from lusid.models.resource_id import ResourceId

class PortfolioReconciliationRequest(BaseModel):
    """
    PortfolioReconciliationRequest
    """
    portfolio_id: ResourceId = Field(..., alias="portfolioId")
    effective_at: constr(strict=True, min_length=1) = Field(..., alias="effectiveAt", description="The effective date of the portfolio")
    as_at: Optional[datetime] = Field(None, alias="asAt", description="Optional. The AsAt date of the portfolio")
    __properties = ["portfolioId", "effectiveAt", "asAt"]

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
    def from_json(cls, json_str: str) -> PortfolioReconciliationRequest:
        """Create an instance of PortfolioReconciliationRequest from a JSON string"""
        return cls.from_dict(json.loads(json_str))

    def to_dict(self):
        """Returns the dictionary representation of the model using alias"""
        _dict = self.dict(by_alias=True,
                          exclude={
                          },
                          exclude_none=True)
        # override the default output from pydantic by calling `to_dict()` of portfolio_id
        if self.portfolio_id:
            _dict['portfolioId'] = self.portfolio_id.to_dict()
        # set to None if as_at (nullable) is None
        # and __fields_set__ contains the field
        if self.as_at is None and "as_at" in self.__fields_set__:
            _dict['asAt'] = None

        return _dict

    @classmethod
    def from_dict(cls, obj: dict) -> PortfolioReconciliationRequest:
        """Create an instance of PortfolioReconciliationRequest from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return PortfolioReconciliationRequest.parse_obj(obj)

        _obj = PortfolioReconciliationRequest.parse_obj({
            "portfolio_id": ResourceId.from_dict(obj.get("portfolioId")) if obj.get("portfolioId") is not None else None,
            "effective_at": obj.get("effectiveAt"),
            "as_at": obj.get("asAt")
        })
        return _obj
