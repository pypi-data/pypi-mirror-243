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
from lusid.models.described_address_key import DescribedAddressKey
from lusid.models.economic_dependency import EconomicDependency
from lusid.models.link import Link

class InstrumentCapabilities(BaseModel):
    """
    Instrument capabilities containing useful information about the instrument and the model. This includes  - features corresponding to the instrument i.e. Optionality:American, Other:InflationLinked  - supported addresses (if model provided) i.e. Valuation/Pv, Valuation/DirtyPriceKey, Valuation/Accrued  - economic dependencies (if model provided) i.e. Cash:USD, Fx:GBP.USD, Rates:GBP.GBPOIS  # noqa: E501
    """
    instrument_id: Optional[StrictStr] = Field(None, alias="instrumentId", description="The Lusid instrument id for the instrument e.g. 'LUID_00003D4X'.")
    model: Optional[StrictStr] = Field(None, description="The pricing model e.g. 'Discounting'.")
    features: Optional[Dict[str, StrictStr]] = Field(None, description="Features of the instrument describing its optionality, payoff type and more e.g. 'Instrument/Features/Exercise: American', 'Instrument/Features/Product: Option'")
    supported_addresses: Optional[conlist(DescribedAddressKey)] = Field(None, alias="supportedAddresses", description="Queryable addresses supported by the model, e.g. 'Valuation/Pv', 'Valuation/Accrued'.")
    economic_dependencies: Optional[conlist(EconomicDependency)] = Field(None, alias="economicDependencies", description="Economic dependencies for the model, e.g. 'Fx:GBP.USD', 'Cash:GBP', 'Rates:GBP.GBPOIS'.")
    links: Optional[conlist(Link)] = None
    __properties = ["instrumentId", "model", "features", "supportedAddresses", "economicDependencies", "links"]

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
    def from_json(cls, json_str: str) -> InstrumentCapabilities:
        """Create an instance of InstrumentCapabilities from a JSON string"""
        return cls.from_dict(json.loads(json_str))

    def to_dict(self):
        """Returns the dictionary representation of the model using alias"""
        _dict = self.dict(by_alias=True,
                          exclude={
                          },
                          exclude_none=True)
        # override the default output from pydantic by calling `to_dict()` of each item in supported_addresses (list)
        _items = []
        if self.supported_addresses:
            for _item in self.supported_addresses:
                if _item:
                    _items.append(_item.to_dict())
            _dict['supportedAddresses'] = _items
        # override the default output from pydantic by calling `to_dict()` of each item in economic_dependencies (list)
        _items = []
        if self.economic_dependencies:
            for _item in self.economic_dependencies:
                if _item:
                    _items.append(_item.to_dict())
            _dict['economicDependencies'] = _items
        # override the default output from pydantic by calling `to_dict()` of each item in links (list)
        _items = []
        if self.links:
            for _item in self.links:
                if _item:
                    _items.append(_item.to_dict())
            _dict['links'] = _items
        # set to None if instrument_id (nullable) is None
        # and __fields_set__ contains the field
        if self.instrument_id is None and "instrument_id" in self.__fields_set__:
            _dict['instrumentId'] = None

        # set to None if model (nullable) is None
        # and __fields_set__ contains the field
        if self.model is None and "model" in self.__fields_set__:
            _dict['model'] = None

        # set to None if features (nullable) is None
        # and __fields_set__ contains the field
        if self.features is None and "features" in self.__fields_set__:
            _dict['features'] = None

        # set to None if supported_addresses (nullable) is None
        # and __fields_set__ contains the field
        if self.supported_addresses is None and "supported_addresses" in self.__fields_set__:
            _dict['supportedAddresses'] = None

        # set to None if economic_dependencies (nullable) is None
        # and __fields_set__ contains the field
        if self.economic_dependencies is None and "economic_dependencies" in self.__fields_set__:
            _dict['economicDependencies'] = None

        # set to None if links (nullable) is None
        # and __fields_set__ contains the field
        if self.links is None and "links" in self.__fields_set__:
            _dict['links'] = None

        return _dict

    @classmethod
    def from_dict(cls, obj: dict) -> InstrumentCapabilities:
        """Create an instance of InstrumentCapabilities from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return InstrumentCapabilities.parse_obj(obj)

        _obj = InstrumentCapabilities.parse_obj({
            "instrument_id": obj.get("instrumentId"),
            "model": obj.get("model"),
            "features": obj.get("features"),
            "supported_addresses": [DescribedAddressKey.from_dict(_item) for _item in obj.get("supportedAddresses")] if obj.get("supportedAddresses") is not None else None,
            "economic_dependencies": [EconomicDependency.from_dict(_item) for _item in obj.get("economicDependencies")] if obj.get("economicDependencies") is not None else None,
            "links": [Link.from_dict(_item) for _item in obj.get("links")] if obj.get("links") is not None else None
        })
        return _obj
