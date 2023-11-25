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
from pydantic import Field, StrictStr, conlist, constr, validator
from lusid.models.level_step import LevelStep
from lusid.models.schedule import Schedule

class StepSchedule(Schedule):
    """
    Schedule that steps at known dated points in time.  Used in representation of a sinking bond, also called amortisation, steps in coupons for fixed bonds and spreads for floating bonds.  # noqa: E501
    """
    level_type: constr(strict=True, min_length=1) = Field(..., alias="levelType", description="The type of shift or adjustment that the quantity represents.    Supported string (enumeration) values are: [Absolute, AbsoluteShift, Percentage, AbsolutePercentage].")
    step_schedule_type: constr(strict=True, min_length=1) = Field(..., alias="stepScheduleType", description="The type of step that this schedule is for.  Supported string (enumeration) values are: [Coupon, Notional, Spread].")
    steps: conlist(LevelStep) = Field(..., description="The level steps which are applied.")
    schedule_type: StrictStr = Field(..., alias="scheduleType", description="The available values are: FixedSchedule, FloatSchedule, OptionalitySchedule, StepSchedule, Exercise, FxRateSchedule, Invalid")
    additional_properties: Dict[str, Any] = {}
    __properties = ["scheduleType", "levelType", "stepScheduleType", "steps"]

    @validator('schedule_type')
    def schedule_type_validate_enum(cls, value):
        """Validates the enum"""
        if value not in ('FixedSchedule', 'FloatSchedule', 'OptionalitySchedule', 'StepSchedule', 'Exercise', 'FxRateSchedule', 'Invalid'):
            raise ValueError("must be one of enum values ('FixedSchedule', 'FloatSchedule', 'OptionalitySchedule', 'StepSchedule', 'Exercise', 'FxRateSchedule', 'Invalid')")
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
    def from_json(cls, json_str: str) -> StepSchedule:
        """Create an instance of StepSchedule from a JSON string"""
        return cls.from_dict(json.loads(json_str))

    def to_dict(self):
        """Returns the dictionary representation of the model using alias"""
        _dict = self.dict(by_alias=True,
                          exclude={
                            "additional_properties"
                          },
                          exclude_none=True)
        # override the default output from pydantic by calling `to_dict()` of each item in steps (list)
        _items = []
        if self.steps:
            for _item in self.steps:
                if _item:
                    _items.append(_item.to_dict())
            _dict['steps'] = _items
        # puts key-value pairs in additional_properties in the top level
        if self.additional_properties is not None:
            for _key, _value in self.additional_properties.items():
                _dict[_key] = _value

        return _dict

    @classmethod
    def from_dict(cls, obj: dict) -> StepSchedule:
        """Create an instance of StepSchedule from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return StepSchedule.parse_obj(obj)

        _obj = StepSchedule.parse_obj({
            "schedule_type": obj.get("scheduleType"),
            "level_type": obj.get("levelType"),
            "step_schedule_type": obj.get("stepScheduleType"),
            "steps": [LevelStep.from_dict(_item) for _item in obj.get("steps")] if obj.get("steps") is not None else None
        })
        # store additional fields in additional_properties
        for _key in obj.keys():
            if _key not in cls.__properties:
                _obj.additional_properties[_key] = obj.get(_key)

        return _obj
