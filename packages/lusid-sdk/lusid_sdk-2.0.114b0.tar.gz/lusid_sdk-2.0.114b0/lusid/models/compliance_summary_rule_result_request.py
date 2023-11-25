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


from typing import Any, Dict, List
from pydantic import BaseModel, Field, StrictStr, conlist, constr
from lusid.models.compliance_rule_breakdown_request import ComplianceRuleBreakdownRequest
from lusid.models.resource_id import ResourceId

class ComplianceSummaryRuleResultRequest(BaseModel):
    """
    ComplianceSummaryRuleResultRequest
    """
    rule_id: ResourceId = Field(..., alias="ruleId")
    template_id: ResourceId = Field(..., alias="templateId")
    variation: constr(strict=True, max_length=6000, min_length=0) = Field(...)
    rule_status: constr(strict=True, max_length=6000, min_length=0) = Field(..., alias="ruleStatus")
    affected_portfolios: conlist(ResourceId) = Field(..., alias="affectedPortfolios")
    affected_orders: conlist(ResourceId) = Field(..., alias="affectedOrders")
    parameters_used: Dict[str, StrictStr] = Field(..., alias="parametersUsed")
    rule_breakdown: Dict[str, ComplianceRuleBreakdownRequest] = Field(..., alias="ruleBreakdown")
    __properties = ["ruleId", "templateId", "variation", "ruleStatus", "affectedPortfolios", "affectedOrders", "parametersUsed", "ruleBreakdown"]

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
    def from_json(cls, json_str: str) -> ComplianceSummaryRuleResultRequest:
        """Create an instance of ComplianceSummaryRuleResultRequest from a JSON string"""
        return cls.from_dict(json.loads(json_str))

    def to_dict(self):
        """Returns the dictionary representation of the model using alias"""
        _dict = self.dict(by_alias=True,
                          exclude={
                          },
                          exclude_none=True)
        # override the default output from pydantic by calling `to_dict()` of rule_id
        if self.rule_id:
            _dict['ruleId'] = self.rule_id.to_dict()
        # override the default output from pydantic by calling `to_dict()` of template_id
        if self.template_id:
            _dict['templateId'] = self.template_id.to_dict()
        # override the default output from pydantic by calling `to_dict()` of each item in affected_portfolios (list)
        _items = []
        if self.affected_portfolios:
            for _item in self.affected_portfolios:
                if _item:
                    _items.append(_item.to_dict())
            _dict['affectedPortfolios'] = _items
        # override the default output from pydantic by calling `to_dict()` of each item in affected_orders (list)
        _items = []
        if self.affected_orders:
            for _item in self.affected_orders:
                if _item:
                    _items.append(_item.to_dict())
            _dict['affectedOrders'] = _items
        # override the default output from pydantic by calling `to_dict()` of each value in rule_breakdown (dict)
        _field_dict = {}
        if self.rule_breakdown:
            for _key in self.rule_breakdown:
                if self.rule_breakdown[_key]:
                    _field_dict[_key] = self.rule_breakdown[_key].to_dict()
            _dict['ruleBreakdown'] = _field_dict
        return _dict

    @classmethod
    def from_dict(cls, obj: dict) -> ComplianceSummaryRuleResultRequest:
        """Create an instance of ComplianceSummaryRuleResultRequest from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return ComplianceSummaryRuleResultRequest.parse_obj(obj)

        _obj = ComplianceSummaryRuleResultRequest.parse_obj({
            "rule_id": ResourceId.from_dict(obj.get("ruleId")) if obj.get("ruleId") is not None else None,
            "template_id": ResourceId.from_dict(obj.get("templateId")) if obj.get("templateId") is not None else None,
            "variation": obj.get("variation"),
            "rule_status": obj.get("ruleStatus"),
            "affected_portfolios": [ResourceId.from_dict(_item) for _item in obj.get("affectedPortfolios")] if obj.get("affectedPortfolios") is not None else None,
            "affected_orders": [ResourceId.from_dict(_item) for _item in obj.get("affectedOrders")] if obj.get("affectedOrders") is not None else None,
            "parameters_used": obj.get("parametersUsed"),
            "rule_breakdown": dict(
                (_k, ComplianceRuleBreakdownRequest.from_dict(_v))
                for _k, _v in obj.get("ruleBreakdown").items()
            )
            if obj.get("ruleBreakdown") is not None
            else None
        })
        return _obj
