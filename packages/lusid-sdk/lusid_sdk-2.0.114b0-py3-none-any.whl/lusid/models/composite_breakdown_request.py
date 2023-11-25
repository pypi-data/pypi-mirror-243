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
from pydantic import BaseModel, Field, StrictStr, conlist, constr
from lusid.models.resource_id import ResourceId

class CompositeBreakdownRequest(BaseModel):
    """
    The request used in the GetCompositeBreakdown.  # noqa: E501
    """
    return_ids: Optional[conlist(ResourceId)] = Field(None, alias="returnIds", description="The Scope and code of the returns.")
    recipe_id: Optional[ResourceId] = Field(None, alias="recipeId")
    composite_method: Optional[StrictStr] = Field(None, alias="compositeMethod", description="The method used to calculate the Portfolio performance: Equal/Asset.")
    period: Optional[StrictStr] = Field(None, description="The type of the returns used to calculate the aggregation result: Daily/Monthly.")
    holiday_calendars: Optional[conlist(StrictStr)] = Field(None, alias="holidayCalendars", description="The holiday calendar(s) that should be used in determining the date schedule. Holiday calendar(s) are supplied by their codes, for example, 'CoppClark'. Note that when the calendars are not available (e.g. when the user has insufficient permissions), a recipe setting will be used to determine whether the whole batch should then fail or whether the calendar not being available should simply be ignored.")
    currency: Optional[constr(strict=True, max_length=6000, min_length=0)] = Field(None, description="Optional - either a string or a property. If provided, the results will be converted to the specified currency")
    __properties = ["returnIds", "recipeId", "compositeMethod", "period", "holidayCalendars", "currency"]

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
    def from_json(cls, json_str: str) -> CompositeBreakdownRequest:
        """Create an instance of CompositeBreakdownRequest from a JSON string"""
        return cls.from_dict(json.loads(json_str))

    def to_dict(self):
        """Returns the dictionary representation of the model using alias"""
        _dict = self.dict(by_alias=True,
                          exclude={
                          },
                          exclude_none=True)
        # override the default output from pydantic by calling `to_dict()` of each item in return_ids (list)
        _items = []
        if self.return_ids:
            for _item in self.return_ids:
                if _item:
                    _items.append(_item.to_dict())
            _dict['returnIds'] = _items
        # override the default output from pydantic by calling `to_dict()` of recipe_id
        if self.recipe_id:
            _dict['recipeId'] = self.recipe_id.to_dict()
        # set to None if return_ids (nullable) is None
        # and __fields_set__ contains the field
        if self.return_ids is None and "return_ids" in self.__fields_set__:
            _dict['returnIds'] = None

        # set to None if composite_method (nullable) is None
        # and __fields_set__ contains the field
        if self.composite_method is None and "composite_method" in self.__fields_set__:
            _dict['compositeMethod'] = None

        # set to None if period (nullable) is None
        # and __fields_set__ contains the field
        if self.period is None and "period" in self.__fields_set__:
            _dict['period'] = None

        # set to None if holiday_calendars (nullable) is None
        # and __fields_set__ contains the field
        if self.holiday_calendars is None and "holiday_calendars" in self.__fields_set__:
            _dict['holidayCalendars'] = None

        # set to None if currency (nullable) is None
        # and __fields_set__ contains the field
        if self.currency is None and "currency" in self.__fields_set__:
            _dict['currency'] = None

        return _dict

    @classmethod
    def from_dict(cls, obj: dict) -> CompositeBreakdownRequest:
        """Create an instance of CompositeBreakdownRequest from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return CompositeBreakdownRequest.parse_obj(obj)

        _obj = CompositeBreakdownRequest.parse_obj({
            "return_ids": [ResourceId.from_dict(_item) for _item in obj.get("returnIds")] if obj.get("returnIds") is not None else None,
            "recipe_id": ResourceId.from_dict(obj.get("recipeId")) if obj.get("recipeId") is not None else None,
            "composite_method": obj.get("compositeMethod"),
            "period": obj.get("period"),
            "holiday_calendars": obj.get("holidayCalendars"),
            "currency": obj.get("currency")
        })
        return _obj
