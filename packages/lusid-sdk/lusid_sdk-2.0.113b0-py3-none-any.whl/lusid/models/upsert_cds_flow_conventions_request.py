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


from typing import Any, Dict, Optional
from pydantic import BaseModel, Field
from lusid.models.cds_flow_conventions import CdsFlowConventions

class UpsertCdsFlowConventionsRequest(BaseModel):
    """
    CDS Flow convention that is to be stored in the convention data store.  Only one of these must be present.  # noqa: E501
    """
    cds_flow_conventions: Optional[CdsFlowConventions] = Field(None, alias="cdsFlowConventions")
    __properties = ["cdsFlowConventions"]

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
    def from_json(cls, json_str: str) -> UpsertCdsFlowConventionsRequest:
        """Create an instance of UpsertCdsFlowConventionsRequest from a JSON string"""
        return cls.from_dict(json.loads(json_str))

    def to_dict(self):
        """Returns the dictionary representation of the model using alias"""
        _dict = self.dict(by_alias=True,
                          exclude={
                          },
                          exclude_none=True)
        # override the default output from pydantic by calling `to_dict()` of cds_flow_conventions
        if self.cds_flow_conventions:
            _dict['cdsFlowConventions'] = self.cds_flow_conventions.to_dict()
        return _dict

    @classmethod
    def from_dict(cls, obj: dict) -> UpsertCdsFlowConventionsRequest:
        """Create an instance of UpsertCdsFlowConventionsRequest from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return UpsertCdsFlowConventionsRequest.parse_obj(obj)

        _obj = UpsertCdsFlowConventionsRequest.parse_obj({
            "cds_flow_conventions": CdsFlowConventions.from_dict(obj.get("cdsFlowConventions")) if obj.get("cdsFlowConventions") is not None else None
        })
        return _obj
