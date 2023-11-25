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
from pydantic import Field, StrictStr, conlist, validator
from lusid.models.cash_flow_value import CashFlowValue
from lusid.models.result_value import ResultValue

class CashFlowValueSet(ResultValue):
    """
    Result value for a collection of cash flow values  # noqa: E501
    """
    cashflows: Optional[conlist(CashFlowValue)] = Field(None, description="The set of cash flows in the result")
    result_value_type: StrictStr = Field(..., alias="resultValueType", description="The available values are: ResultValue, ResultValueDictionary, ResultValue0D, ResultValueDecimal, ResultValueInt, ResultValueString, ResultValueBool, ResultValueCurrency, CashFlowValue, CashFlowValueSet, ResultValueLifeCycleEventValue, ResultValueDateTimeOffset")
    additional_properties: Dict[str, Any] = {}
    __properties = ["resultValueType", "cashflows"]

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
    def from_json(cls, json_str: str) -> CashFlowValueSet:
        """Create an instance of CashFlowValueSet from a JSON string"""
        return cls.from_dict(json.loads(json_str))

    def to_dict(self):
        """Returns the dictionary representation of the model using alias"""
        _dict = self.dict(by_alias=True,
                          exclude={
                            "additional_properties"
                          },
                          exclude_none=True)
        # override the default output from pydantic by calling `to_dict()` of each item in cashflows (list)
        _items = []
        if self.cashflows:
            for _item in self.cashflows:
                if _item:
                    _items.append(_item.to_dict())
            _dict['cashflows'] = _items
        # puts key-value pairs in additional_properties in the top level
        if self.additional_properties is not None:
            for _key, _value in self.additional_properties.items():
                _dict[_key] = _value

        # set to None if cashflows (nullable) is None
        # and __fields_set__ contains the field
        if self.cashflows is None and "cashflows" in self.__fields_set__:
            _dict['cashflows'] = None

        return _dict

    @classmethod
    def from_dict(cls, obj: dict) -> CashFlowValueSet:
        """Create an instance of CashFlowValueSet from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return CashFlowValueSet.parse_obj(obj)

        _obj = CashFlowValueSet.parse_obj({
            "result_value_type": obj.get("resultValueType"),
            "cashflows": [CashFlowValue.from_dict(_item) for _item in obj.get("cashflows")] if obj.get("cashflows") is not None else None
        })
        # store additional fields in additional_properties
        for _key in obj.keys():
            if _key not in cls.__properties:
                _obj.additional_properties[_key] = obj.get(_key)

        return _obj
