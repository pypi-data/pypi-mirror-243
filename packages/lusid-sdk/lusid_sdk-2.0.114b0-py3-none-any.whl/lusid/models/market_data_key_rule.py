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

from datetime import datetime
from typing import Any, Dict, Optional
from pydantic import BaseModel, Field, StrictStr, constr, validator

class MarketDataKeyRule(BaseModel):
    """
    When performing analytics, instruments and models have dependencies on market data.  A market data key rule essentially tells lusid to \"resolve dependencies matching the pattern 'X' using data of the form 'Y'\".  The parameter 'X' is defined by the key of the key rule, and might specify \"all USD rates curves\" or \"all RIC-based prices\".  The parameter 'Y' is defined by the remaining fields of the key rule, and allows the user to configure things such as  where to look for data, what sort of data should be looked for (e.g. bid/mid/ask), and how old the data is allowed to be.  # noqa: E501
    """
    key: constr(strict=True, max_length=128, min_length=0) = Field(..., description="A dot-separated string that defines a pattern for matching market data dependencies.  The form of the string depends on the type of the dependency; see below for basic types and the Knowledge Base for further info.  Quote lookup: \"Quote.{CodeType}.*\" e.g. \"Quote.RIC.*\" refers to 'any RIC quote'  Fx rates: \"Fx.CurrencyPair.*\", which refers to 'any FX rate'  Discounting curves: \"Rates.{Currency}.{Currency}OIS e.g. \"Rates.USD.USDOIS\" refers to the OIS USD discounting curve                For non-fx and non-quote rules, trailing parameters can be replaced by the wildcard character '*'.  e.g. \"Rates.*.*\" matches any dependency on a discounting curve.")
    supplier: constr(strict=True, max_length=32, min_length=0) = Field(..., description="The market data supplier (where the data comes from)")
    data_scope: constr(strict=True, max_length=256, min_length=1) = Field(..., alias="dataScope", description="The scope in which the data should be found when using this rule.")
    quote_type: StrictStr = Field(..., alias="quoteType", description="The available values are: Price, Spread, Rate, LogNormalVol, NormalVol, ParSpread, IsdaSpread, Upfront, Index, Ratio, Delta, PoolFactor, InflationAssumption, DirtyPrice")
    field: Optional[constr(strict=True, max_length=32, min_length=0)] = Field(None, description="The conceptual qualification for the field, typically 'bid', 'mid' (default), or 'ask', but can also be 'open', 'close', etc.  When resolving quotes from LUSID's database, only quotes whose Field is identical to the Field specified here  will be accepted as market data.  When resolving data from an external supplier, the Field must be one of a defined set for the given supplier.                Note: Applies to the retrieval of quotes only. Has no impact on the resolution of complex market data.")
    quote_interval: Optional[constr(strict=True, max_length=16, min_length=0)] = Field(None, alias="quoteInterval", description="Shorthand for the time interval used to select market data. This must be a dot-separated string              nominating a start and end date, for example '5D.0D' to look back 5 days from today (0 days ago). The syntax              is <i>int</i><i>char</i>.<i>int</i><i>char</i>, where <i>char</i> is one of              D(ay), Bd(business day), W(eek), M(onth) or Y(ear).              Business days are calculated using the calendars specified on the Valuation Request.              If no calendar is provided in the request, then it will default to only skipping weekends.              For example, if the valuation date is a Monday, then a quote interval of \"1Bd\" would behave as \"3D\",              looking back to the Friday. Data with effectiveAt on the weekend will still be found in that window.")
    as_at: Optional[datetime] = Field(None, alias="asAt", description="The AsAt predicate specification.")
    price_source: Optional[constr(strict=True, max_length=256, min_length=0)] = Field(None, alias="priceSource", description="The source of the quote. For a given provider/supplier of market data there may be an additional qualifier, e.g. the exchange or bank that provided the quote")
    mask: Optional[constr(strict=True, max_length=256, min_length=0)] = Field(None, description="Allows for partial or complete override of the market asset resolved for a dependency  Either a named override or a dot separated string (A.B.C.D.*).  e.g. for Rates curve 'EUR.*' will replace the resolve MarketAsset 'GBP/12M', 'GBP/3M' with the EUR equivalent, if there  are no wildcards in the mask, the mask is taken as the MarketAsset for any dependency matching the rule.")
    source_system: Optional[constr(strict=True, max_length=256, min_length=0)] = Field(None, alias="sourceSystem", description="If set, this parameter will seek an external source of market data.  Optional and, if omitted, will default to \"Lusid\".  This means that data will be retrieved from the LUSID Quote Store and LUSID Complex Market Data Store.                This can be set to \"MarketDataOverrides\" if Supplier is set to \"Client\".")
    __properties = ["key", "supplier", "dataScope", "quoteType", "field", "quoteInterval", "asAt", "priceSource", "mask", "sourceSystem"]

    @validator('data_scope')
    def data_scope_validate_regular_expression(cls, value):
        """Validates the regular expression"""
        if not re.match(r"^[a-zA-Z0-9\-_]+$", value):
            raise ValueError(r"must validate the regular expression /^[a-zA-Z0-9\-_]+$/")
        return value

    @validator('quote_type')
    def quote_type_validate_enum(cls, value):
        """Validates the enum"""
        if value not in ('Price', 'Spread', 'Rate', 'LogNormalVol', 'NormalVol', 'ParSpread', 'IsdaSpread', 'Upfront', 'Index', 'Ratio', 'Delta', 'PoolFactor', 'InflationAssumption', 'DirtyPrice'):
            raise ValueError("must be one of enum values ('Price', 'Spread', 'Rate', 'LogNormalVol', 'NormalVol', 'ParSpread', 'IsdaSpread', 'Upfront', 'Index', 'Ratio', 'Delta', 'PoolFactor', 'InflationAssumption', 'DirtyPrice')")
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
    def from_json(cls, json_str: str) -> MarketDataKeyRule:
        """Create an instance of MarketDataKeyRule from a JSON string"""
        return cls.from_dict(json.loads(json_str))

    def to_dict(self):
        """Returns the dictionary representation of the model using alias"""
        _dict = self.dict(by_alias=True,
                          exclude={
                          },
                          exclude_none=True)
        # set to None if field (nullable) is None
        # and __fields_set__ contains the field
        if self.field is None and "field" in self.__fields_set__:
            _dict['field'] = None

        # set to None if quote_interval (nullable) is None
        # and __fields_set__ contains the field
        if self.quote_interval is None and "quote_interval" in self.__fields_set__:
            _dict['quoteInterval'] = None

        # set to None if as_at (nullable) is None
        # and __fields_set__ contains the field
        if self.as_at is None and "as_at" in self.__fields_set__:
            _dict['asAt'] = None

        # set to None if price_source (nullable) is None
        # and __fields_set__ contains the field
        if self.price_source is None and "price_source" in self.__fields_set__:
            _dict['priceSource'] = None

        # set to None if mask (nullable) is None
        # and __fields_set__ contains the field
        if self.mask is None and "mask" in self.__fields_set__:
            _dict['mask'] = None

        # set to None if source_system (nullable) is None
        # and __fields_set__ contains the field
        if self.source_system is None and "source_system" in self.__fields_set__:
            _dict['sourceSystem'] = None

        return _dict

    @classmethod
    def from_dict(cls, obj: dict) -> MarketDataKeyRule:
        """Create an instance of MarketDataKeyRule from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return MarketDataKeyRule.parse_obj(obj)

        _obj = MarketDataKeyRule.parse_obj({
            "key": obj.get("key"),
            "supplier": obj.get("supplier"),
            "data_scope": obj.get("dataScope"),
            "quote_type": obj.get("quoteType"),
            "field": obj.get("field"),
            "quote_interval": obj.get("quoteInterval"),
            "as_at": obj.get("asAt"),
            "price_source": obj.get("priceSource"),
            "mask": obj.get("mask"),
            "source_system": obj.get("sourceSystem")
        })
        return _obj
