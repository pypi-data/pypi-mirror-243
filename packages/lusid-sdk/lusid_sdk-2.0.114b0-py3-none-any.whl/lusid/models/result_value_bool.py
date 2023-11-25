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
from pydantic import Field, StrictBool, StrictStr, validator
from lusid.models.result_value import ResultValue

class ResultValueBool(ResultValue):
    """
    A simple result for a boolean value  # noqa: E501
    """
    value: Optional[StrictBool] = Field(None, description="The value itself")
    result_value_type: StrictStr = Field(..., alias="resultValueType", description="The available values are: ResultValue, ResultValueDictionary, ResultValue0D, ResultValueDecimal, ResultValueInt, ResultValueString, ResultValueBool, ResultValueCurrency, CashFlowValue, CashFlowValueSet, ResultValueLifeCycleEventValue, ResultValueDateTimeOffset")
    additional_properties: Dict[str, Any] = {}
    __properties = ["resultValueType", "value"]

    @validator('result_value_type')
    def result_value_type_validate_enum(cls, value):
        """Validates the enum"""
        if value not in ('ResultValue', 'ResultValueDictionary', 'ResultValue0D', 'ResultValueDecimal', 'ResultValueInt', 'ResultValueString', 'ResultValueBool', 'ResultValueCurrency', 'CashFlowValue', 'CashFlowValueSet', 'ResultValueLifeCycleEventValue', 'ResultValueDateTimeOffset'):
            raise ValueError("must be one of enum values ('ResultValue', 'ResultValueDictionary', 'ResultValue0D', 'ResultValueDecimal', 'ResultValueInt', 'ResultValueString', 'ResultValueBool', 'ResultValueCurrency', 'CashFlowValue', 'CashFlowValueSet', 'ResultValueLifeCycleEventValue', 'ResultValueDateTimeOffset')")
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
    def from_json(cls, json_str: str) -> ResultValueBool:
        """Create an instance of ResultValueBool from a JSON string"""
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
    def from_dict(cls, obj: dict) -> ResultValueBool:
        """Create an instance of ResultValueBool from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return ResultValueBool.parse_obj(obj)

        _obj = ResultValueBool.parse_obj({
            "result_value_type": obj.get("resultValueType"),
            "value": obj.get("value")
        })
        # store additional fields in additional_properties
        for _key in obj.keys():
            if _key not in cls.__properties:
                _obj.additional_properties[_key] = obj.get(_key)

        return _obj
