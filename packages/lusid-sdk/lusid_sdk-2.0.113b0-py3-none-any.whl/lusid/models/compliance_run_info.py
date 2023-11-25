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
from typing import Any, Dict
from pydantic import BaseModel, Field, StrictBool, constr

class ComplianceRunInfo(BaseModel):
    """
    ComplianceRunInfo
    """
    run_id: constr(strict=True, min_length=1) = Field(..., alias="runId", description="The unique identifier of a compliance run")
    instigated_at: datetime = Field(..., alias="instigatedAt", description="The time the compliance run was launched (e.g. button pressed). Currently it is also both the as at and effective at time in whichthe rule set and portfolio data (including any pending trades if the run is pretrade) is taken for the caluation, although it may be possible to run compliance for historical effective at and as at dates in the future.")
    completed_at: datetime = Field(..., alias="completedAt", description="The time the compliance run calculation was completed")
    schedule: constr(strict=True, min_length=1) = Field(..., description="Whether the compliance run was pre or post trade")
    all_rules_passed: StrictBool = Field(..., alias="allRulesPassed", description="True if all rules passed, for all the portfolios they were assigned to")
    has_results: StrictBool = Field(..., alias="hasResults", description="False when no results have been returned eg. when no rules exist")
    as_at: datetime = Field(..., alias="asAt", description="Legacy AsAt time for backwards compatibility")
    __properties = ["runId", "instigatedAt", "completedAt", "schedule", "allRulesPassed", "hasResults", "asAt"]

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
    def from_json(cls, json_str: str) -> ComplianceRunInfo:
        """Create an instance of ComplianceRunInfo from a JSON string"""
        return cls.from_dict(json.loads(json_str))

    def to_dict(self):
        """Returns the dictionary representation of the model using alias"""
        _dict = self.dict(by_alias=True,
                          exclude={
                          },
                          exclude_none=True)
        return _dict

    @classmethod
    def from_dict(cls, obj: dict) -> ComplianceRunInfo:
        """Create an instance of ComplianceRunInfo from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return ComplianceRunInfo.parse_obj(obj)

        _obj = ComplianceRunInfo.parse_obj({
            "run_id": obj.get("runId"),
            "instigated_at": obj.get("instigatedAt"),
            "completed_at": obj.get("completedAt"),
            "schedule": obj.get("schedule"),
            "all_rules_passed": obj.get("allRulesPassed"),
            "has_results": obj.get("hasResults"),
            "as_at": obj.get("asAt")
        })
        return _obj
