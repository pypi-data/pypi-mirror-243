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
from pydantic import BaseModel, Field, StrictStr, conlist
from lusid.models.instrument_payment_diary_row import InstrumentPaymentDiaryRow

class InstrumentPaymentDiaryLeg(BaseModel):
    """
    A leg containing a set of cashflows.  # noqa: E501
    """
    leg_id: Optional[StrictStr] = Field(None, alias="legId", description="Identifier for the leg of a payment diary.")
    rows: Optional[conlist(InstrumentPaymentDiaryRow)] = Field(None, description="List of individual cashflows within the payment diary.")
    __properties = ["legId", "rows"]

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
    def from_json(cls, json_str: str) -> InstrumentPaymentDiaryLeg:
        """Create an instance of InstrumentPaymentDiaryLeg from a JSON string"""
        return cls.from_dict(json.loads(json_str))

    def to_dict(self):
        """Returns the dictionary representation of the model using alias"""
        _dict = self.dict(by_alias=True,
                          exclude={
                          },
                          exclude_none=True)
        # override the default output from pydantic by calling `to_dict()` of each item in rows (list)
        _items = []
        if self.rows:
            for _item in self.rows:
                if _item:
                    _items.append(_item.to_dict())
            _dict['rows'] = _items
        # set to None if leg_id (nullable) is None
        # and __fields_set__ contains the field
        if self.leg_id is None and "leg_id" in self.__fields_set__:
            _dict['legId'] = None

        # set to None if rows (nullable) is None
        # and __fields_set__ contains the field
        if self.rows is None and "rows" in self.__fields_set__:
            _dict['rows'] = None

        return _dict

    @classmethod
    def from_dict(cls, obj: dict) -> InstrumentPaymentDiaryLeg:
        """Create an instance of InstrumentPaymentDiaryLeg from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return InstrumentPaymentDiaryLeg.parse_obj(obj)

        _obj = InstrumentPaymentDiaryLeg.parse_obj({
            "leg_id": obj.get("legId"),
            "rows": [InstrumentPaymentDiaryRow.from_dict(_item) for _item in obj.get("rows")] if obj.get("rows") is not None else None
        })
        return _obj
