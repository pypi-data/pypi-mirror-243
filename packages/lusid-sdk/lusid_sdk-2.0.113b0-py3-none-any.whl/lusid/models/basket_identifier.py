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
from pydantic import BaseModel, Field, StrictInt, StrictStr

class BasketIdentifier(BaseModel):
    """
    Descriptive information that describes a particular basket of instruments. Most commonly required with a CDS Index or similarly defined instrument.  # noqa: E501
    """
    index: StrictStr = Field(..., description="Index set, e.g. iTraxx or CDX.")
    name: StrictStr = Field(..., description="The index name within the set, e.g. \"MAIN\" or \"Crossover\".")
    region: StrictStr = Field(..., description="Applicable geographic country or region. Typically something like \"Europe\", \"Asia ex-Japan\", \"Japan\" or \"Australia\".")
    series_id: StrictInt = Field(..., alias="seriesId", description="The series identifier.")
    __properties = ["index", "name", "region", "seriesId"]

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
    def from_json(cls, json_str: str) -> BasketIdentifier:
        """Create an instance of BasketIdentifier from a JSON string"""
        return cls.from_dict(json.loads(json_str))

    def to_dict(self):
        """Returns the dictionary representation of the model using alias"""
        _dict = self.dict(by_alias=True,
                          exclude={
                          },
                          exclude_none=True)
        return _dict

    @classmethod
    def from_dict(cls, obj: dict) -> BasketIdentifier:
        """Create an instance of BasketIdentifier from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return BasketIdentifier.parse_obj(obj)

        _obj = BasketIdentifier.parse_obj({
            "index": obj.get("index"),
            "name": obj.get("name"),
            "region": obj.get("region"),
            "series_id": obj.get("seriesId")
        })
        return _obj
