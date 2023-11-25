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


from typing import Any, Dict, Union
from pydantic import BaseModel, Field, StrictFloat, StrictInt, StrictStr

class CorporateActionTransitionComponentRequest(BaseModel):
    """
    A single transition component request, when grouped with other transition component requests a corporate action  transition request is formed.  # noqa: E501
    """
    instrument_identifiers: Dict[str, StrictStr] = Field(..., alias="instrumentIdentifiers", description="Unique instrument identifiers")
    units_factor: Union[StrictFloat, StrictInt] = Field(..., alias="unitsFactor", description="The factor to scale units by")
    cost_factor: Union[StrictFloat, StrictInt] = Field(..., alias="costFactor", description="The factor to scale cost by")
    __properties = ["instrumentIdentifiers", "unitsFactor", "costFactor"]

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
    def from_json(cls, json_str: str) -> CorporateActionTransitionComponentRequest:
        """Create an instance of CorporateActionTransitionComponentRequest from a JSON string"""
        return cls.from_dict(json.loads(json_str))

    def to_dict(self):
        """Returns the dictionary representation of the model using alias"""
        _dict = self.dict(by_alias=True,
                          exclude={
                          },
                          exclude_none=True)
        return _dict

    @classmethod
    def from_dict(cls, obj: dict) -> CorporateActionTransitionComponentRequest:
        """Create an instance of CorporateActionTransitionComponentRequest from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return CorporateActionTransitionComponentRequest.parse_obj(obj)

        _obj = CorporateActionTransitionComponentRequest.parse_obj({
            "instrument_identifiers": obj.get("instrumentIdentifiers"),
            "units_factor": obj.get("unitsFactor"),
            "cost_factor": obj.get("costFactor")
        })
        return _obj
