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
from typing import Any, Dict, Optional, Union
from pydantic import BaseModel, Field, StrictFloat, StrictInt

class CashLadderRecord(BaseModel):
    """
    CashLadderRecord
    """
    effective_date: Optional[datetime] = Field(None, alias="effectiveDate")
    open: Union[StrictFloat, StrictInt] = Field(...)
    activities: Dict[str, Union[StrictFloat, StrictInt]] = Field(...)
    close: Union[StrictFloat, StrictInt] = Field(...)
    __properties = ["effectiveDate", "open", "activities", "close"]

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
    def from_json(cls, json_str: str) -> CashLadderRecord:
        """Create an instance of CashLadderRecord from a JSON string"""
        return cls.from_dict(json.loads(json_str))

    def to_dict(self):
        """Returns the dictionary representation of the model using alias"""
        _dict = self.dict(by_alias=True,
                          exclude={
                          },
                          exclude_none=True)
        return _dict

    @classmethod
    def from_dict(cls, obj: dict) -> CashLadderRecord:
        """Create an instance of CashLadderRecord from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return CashLadderRecord.parse_obj(obj)

        _obj = CashLadderRecord.parse_obj({
            "effective_date": obj.get("effectiveDate"),
            "open": obj.get("open"),
            "activities": obj.get("activities"),
            "close": obj.get("close")
        })
        return _obj
