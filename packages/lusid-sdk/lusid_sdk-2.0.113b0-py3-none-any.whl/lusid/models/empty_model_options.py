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


from typing import Any, Dict
from pydantic import Field, StrictStr, validator
from lusid.models.model_options import ModelOptions

class EmptyModelOptions(ModelOptions):
    """
    EmptyModelOptions
    """
    model_options_type: StrictStr = Field(..., alias="modelOptionsType", description="The available values are: Invalid, OpaqueModelOptions, EmptyModelOptions, IndexModelOptions, FxForwardModelOptions, FundingLegModelOptions, EquityModelOptions, LookUpPricingModelOptions")
    additional_properties: Dict[str, Any] = {}
    __properties = ["modelOptionsType"]

    @validator('model_options_type')
    def model_options_type_validate_enum(cls, value):
        """Validates the enum"""
        if value not in ('Invalid', 'OpaqueModelOptions', 'EmptyModelOptions', 'IndexModelOptions', 'FxForwardModelOptions', 'FundingLegModelOptions', 'EquityModelOptions', 'LookUpPricingModelOptions'):
            raise ValueError("must be one of enum values ('Invalid', 'OpaqueModelOptions', 'EmptyModelOptions', 'IndexModelOptions', 'FxForwardModelOptions', 'FundingLegModelOptions', 'EquityModelOptions', 'LookUpPricingModelOptions')")
        return value

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
    def from_json(cls, json_str: str) -> EmptyModelOptions:
        """Create an instance of EmptyModelOptions from a JSON string"""
        return cls.from_dict(json.loads(json_str))

    def to_dict(self):
        """Returns the dictionary representation of the model using alias"""
        _dict = self.dict(by_alias=True,
                          exclude={
                            "additional_properties"
                          },
                          exclude_none=True)
        # puts key-value pairs in additional_properties in the top level
        if self.additional_properties is not None:
            for _key, _value in self.additional_properties.items():
                _dict[_key] = _value

        return _dict

    @classmethod
    def from_dict(cls, obj: dict) -> EmptyModelOptions:
        """Create an instance of EmptyModelOptions from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return EmptyModelOptions.parse_obj(obj)

        _obj = EmptyModelOptions.parse_obj({
            "model_options_type": obj.get("modelOptionsType")
        })
        # store additional fields in additional_properties
        for _key in obj.keys():
            if _key not in cls.__properties:
                _obj.additional_properties[_key] = obj.get(_key)

        return _obj
