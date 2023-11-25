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


from typing import Any, Dict, Optional, Union
from pydantic import BaseModel, Field, StrictFloat, StrictInt, StrictStr

class RoundingConvention(BaseModel):
    """
    Certain bonds will follow certain rounding conventions.  For example, Thai government bonds will round accrued interest and cashflow values 2dp, whereas for  French government bonds, the rounding is to 7dp.  # noqa: E501
    """
    face_value: Optional[Union[StrictFloat, StrictInt]] = Field(None, alias="faceValue", description="The face value to round against.  The number to be rounded is scaled to this face value before being rounded, and then re-scaled to the holding amount.  For example if rounding an accrued interest value using a FaceValue of 1,000, but 10,000 units are held,  then the initial calculated value would be divided by 10,000, then multiplied by 1,000 and rounded per the convention.  The result of this would then be divided by 1,000 and multiplied by 10,000 to get the final value.")
    precision: Optional[StrictInt] = Field(None, description="The precision of the rounding.  The decimal places to which the rounding takes place.")
    rounding_target: Optional[StrictStr] = Field(None, alias="roundingTarget", description="The target of the rounding convention.  Accepted values are 'AccruedInterest', 'Cashflows', or 'All'    Supported string (enumeration) values are: [All, AccruedInterest, Cashflows].")
    rounding_type: Optional[StrictStr] = Field(None, alias="roundingType", description="The type of rounding.  e.g. Round Up, Round Down    Supported string (enumeration) values are: [Down, Up, Floor, Ceiling, Nearest].")
    __properties = ["faceValue", "precision", "roundingTarget", "roundingType"]

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
    def from_json(cls, json_str: str) -> RoundingConvention:
        """Create an instance of RoundingConvention from a JSON string"""
        return cls.from_dict(json.loads(json_str))

    def to_dict(self):
        """Returns the dictionary representation of the model using alias"""
        _dict = self.dict(by_alias=True,
                          exclude={
                          },
                          exclude_none=True)
        # set to None if rounding_target (nullable) is None
        # and __fields_set__ contains the field
        if self.rounding_target is None and "rounding_target" in self.__fields_set__:
            _dict['roundingTarget'] = None

        # set to None if rounding_type (nullable) is None
        # and __fields_set__ contains the field
        if self.rounding_type is None and "rounding_type" in self.__fields_set__:
            _dict['roundingType'] = None

        return _dict

    @classmethod
    def from_dict(cls, obj: dict) -> RoundingConvention:
        """Create an instance of RoundingConvention from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return RoundingConvention.parse_obj(obj)

        _obj = RoundingConvention.parse_obj({
            "face_value": obj.get("faceValue"),
            "precision": obj.get("precision"),
            "rounding_target": obj.get("roundingTarget"),
            "rounding_type": obj.get("roundingType")
        })
        return _obj
