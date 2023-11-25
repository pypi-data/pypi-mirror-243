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
from pydantic import BaseModel, Field, StrictStr

class LifeCycleEventLineage(BaseModel):
    """
    The lineage of the event value  # noqa: E501
    """
    event_type: Optional[StrictStr] = Field(None, alias="eventType", description="The type of the event")
    instrument_type: Optional[StrictStr] = Field(None, alias="instrumentType", description="The instrument type of the instrument for the event.")
    instrument_id: Optional[StrictStr] = Field(None, alias="instrumentId", description="The LUID of the instrument for the event.")
    leg_id: Optional[StrictStr] = Field(None, alias="legId", description="Leg id for the event.")
    source_transaction_id: Optional[StrictStr] = Field(None, alias="sourceTransactionId", description="The source transaction of the instrument for the event.")
    __properties = ["eventType", "instrumentType", "instrumentId", "legId", "sourceTransactionId"]

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
    def from_json(cls, json_str: str) -> LifeCycleEventLineage:
        """Create an instance of LifeCycleEventLineage from a JSON string"""
        return cls.from_dict(json.loads(json_str))

    def to_dict(self):
        """Returns the dictionary representation of the model using alias"""
        _dict = self.dict(by_alias=True,
                          exclude={
                          },
                          exclude_none=True)
        # set to None if event_type (nullable) is None
        # and __fields_set__ contains the field
        if self.event_type is None and "event_type" in self.__fields_set__:
            _dict['eventType'] = None

        # set to None if instrument_type (nullable) is None
        # and __fields_set__ contains the field
        if self.instrument_type is None and "instrument_type" in self.__fields_set__:
            _dict['instrumentType'] = None

        # set to None if instrument_id (nullable) is None
        # and __fields_set__ contains the field
        if self.instrument_id is None and "instrument_id" in self.__fields_set__:
            _dict['instrumentId'] = None

        # set to None if leg_id (nullable) is None
        # and __fields_set__ contains the field
        if self.leg_id is None and "leg_id" in self.__fields_set__:
            _dict['legId'] = None

        # set to None if source_transaction_id (nullable) is None
        # and __fields_set__ contains the field
        if self.source_transaction_id is None and "source_transaction_id" in self.__fields_set__:
            _dict['sourceTransactionId'] = None

        return _dict

    @classmethod
    def from_dict(cls, obj: dict) -> LifeCycleEventLineage:
        """Create an instance of LifeCycleEventLineage from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return LifeCycleEventLineage.parse_obj(obj)

        _obj = LifeCycleEventLineage.parse_obj({
            "event_type": obj.get("eventType"),
            "instrument_type": obj.get("instrumentType"),
            "instrument_id": obj.get("instrumentId"),
            "leg_id": obj.get("legId"),
            "source_transaction_id": obj.get("sourceTransactionId")
        })
        return _obj
