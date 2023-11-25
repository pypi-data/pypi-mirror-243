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
from pydantic import BaseModel, Field, StrictInt, StrictStr, constr, validator

class IndexConvention(BaseModel):
    """
    A set of conventions that describe the conventions for calculation of payments made on rates interbank lending and similar.  Based on ISDA 2006 conventions and similar documentation. Please see the knowledge base for further documentation.  # noqa: E501
    """
    fixing_reference: constr(strict=True, max_length=64, min_length=0) = Field(..., alias="fixingReference", description="The reference rate name for fixings.")
    publication_day_lag: StrictInt = Field(..., alias="publicationDayLag", description="Number of days between spot and publication of the rate.")
    payment_tenor: constr(strict=True, max_length=32, min_length=0) = Field(..., alias="paymentTenor", description="The tenor of the payment. For an OIS index this is always 1 day. For other indices, e.g. LIBOR it will have a variable tenor typically between 1 day and 1 year.")
    day_count_convention: constr(strict=True, max_length=32, min_length=0) = Field(..., alias="dayCountConvention", description="when calculating the fraction of a year between two dates, what convention is used to represent the number of days in a year  and difference between them.  For more information on day counts, see [knowledge base article KA-01798](https://support.lusid.com/knowledgebase/article/KA-01798)                Supported string (enumeration) values are: [Actual360, Act360, MoneyMarket, Actual365, Act365, Thirty360, ThirtyU360, Bond, ThirtyE360, EuroBond, ActualActual, ActAct, ActActIsda, ActActIsma, ActActIcma, OneOne, Act364, Act365F, Act365L, Act365_25, Act252, Bus252, NL360, NL365].")
    currency: StrictStr = Field(..., description="Currency of the index convention.")
    index_name: Optional[constr(strict=True, max_length=16, min_length=0)] = Field(None, alias="indexName", description="The name of the index for which this represents the conventions of.  For instance, \"SOFR\", \"LIBOR\", \"EURIBOR\", etc.  Defaults to \"INDEX\" if not specified.")
    scope: Optional[constr(strict=True, max_length=256, min_length=1)] = Field(None, description="The scope used when updating or inserting the convention.")
    code: Optional[constr(strict=True, max_length=256, min_length=1)] = Field(None, description="The code of the convention.")
    __properties = ["fixingReference", "publicationDayLag", "paymentTenor", "dayCountConvention", "currency", "indexName", "scope", "code"]

    @validator('scope')
    def scope_validate_regular_expression(cls, value):
        """Validates the regular expression"""
        if value is None:
            return value

        if not re.match(r"^[a-zA-Z0-9\-_]+$", value):
            raise ValueError(r"must validate the regular expression /^[a-zA-Z0-9\-_]+$/")
        return value

    @validator('code')
    def code_validate_regular_expression(cls, value):
        """Validates the regular expression"""
        if value is None:
            return value

        if not re.match(r"^[a-zA-Z0-9\-_]+$", value):
            raise ValueError(r"must validate the regular expression /^[a-zA-Z0-9\-_]+$/")
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
    def from_json(cls, json_str: str) -> IndexConvention:
        """Create an instance of IndexConvention from a JSON string"""
        return cls.from_dict(json.loads(json_str))

    def to_dict(self):
        """Returns the dictionary representation of the model using alias"""
        _dict = self.dict(by_alias=True,
                          exclude={
                          },
                          exclude_none=True)
        # set to None if index_name (nullable) is None
        # and __fields_set__ contains the field
        if self.index_name is None and "index_name" in self.__fields_set__:
            _dict['indexName'] = None

        # set to None if scope (nullable) is None
        # and __fields_set__ contains the field
        if self.scope is None and "scope" in self.__fields_set__:
            _dict['scope'] = None

        # set to None if code (nullable) is None
        # and __fields_set__ contains the field
        if self.code is None and "code" in self.__fields_set__:
            _dict['code'] = None

        return _dict

    @classmethod
    def from_dict(cls, obj: dict) -> IndexConvention:
        """Create an instance of IndexConvention from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return IndexConvention.parse_obj(obj)

        _obj = IndexConvention.parse_obj({
            "fixing_reference": obj.get("fixingReference"),
            "publication_day_lag": obj.get("publicationDayLag"),
            "payment_tenor": obj.get("paymentTenor"),
            "day_count_convention": obj.get("dayCountConvention"),
            "currency": obj.get("currency"),
            "index_name": obj.get("indexName"),
            "scope": obj.get("scope"),
            "code": obj.get("code")
        })
        return _obj
