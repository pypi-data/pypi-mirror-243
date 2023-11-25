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
from pydantic import BaseModel, Field, StrictBool, StrictInt, StrictStr, conlist, constr, validator

class FlowConventions(BaseModel):
    """
    A flow convention defines the specification for generation of the date schedule for a leg or set of cashflows.  It determines the tenor of these and, how to map the unadjusted set of dates to dates which are 'good business  days'. For example, if an unadjusted date falls on a Saturday or a bank holiday, should it be rolled forward  or backward to obtain the adjusted date.  For more information, see https://support.lusid.com/knowledgebase/article/KA-02055/  # noqa: E501
    """
    currency: StrictStr = Field(..., description="Currency of the flow convention.")
    payment_frequency: constr(strict=True, max_length=50, min_length=0) = Field(..., alias="paymentFrequency", description="When generating a multiperiod flow, or when the maturity of the flow is not given but the start date is,  the tenor is the time-step from the anchor-date to the nominal maturity of the flow prior to any adjustment.")
    day_count_convention: constr(strict=True, max_length=50, min_length=0) = Field(..., alias="dayCountConvention", description="when calculating the fraction of a year between two dates, what convention is used to represent the number of days in a year  and difference between them.  For more information on day counts, see [knowledge base article KA-01798](https://support.lusid.com/knowledgebase/article/KA-01798)                Supported string (enumeration) values are: [Actual360, Act360, MoneyMarket, Actual365, Act365, Thirty360, ThirtyU360, Bond, ThirtyE360, EuroBond, ActualActual, ActAct, ActActIsda, ActActIsma, ActActIcma, OneOne, Act364, Act365F, Act365L, Act365_25, Act252, Bus252, NL360, NL365, ActActAFB, Act365Cad, ThirtyActIsda, Thirty365Isda, ThirtyEActIsda, ThirtyE360Isda, ThirtyE365Isda, ThirtyU360EOM].")
    roll_convention: constr(strict=True, max_length=50, min_length=0) = Field(..., alias="rollConvention", description="For backward compatibility, this can either specify a business day convention or a roll convention. If the business  day convention is provided using the BusinessDayConvention property, this must be a valid roll convention.                When used as a roll convention:  The conventions specifying the rule used to generate dates in a schedule.    Supported string (enumeration) values are: [None, EndOfMonth, IMM, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30].                When in backward compatible mode:  Supported string (enumeration) values are: [NoAdjustment, None, Previous, P, Following, F, ModifiedPrevious, MP, ModifiedFollowing, MF, HalfMonthModifiedFollowing].")
    payment_calendars: conlist(StrictStr) = Field(..., alias="paymentCalendars", description="An array of strings denoting holiday calendars that apply to generation of payment schedules.")
    reset_calendars: conlist(StrictStr) = Field(..., alias="resetCalendars", description="An array of strings denoting holiday calendars that apply to generation of reset schedules.")
    settle_days: Optional[StrictInt] = Field(None, alias="settleDays", description="DEPRECATED  Number of Good Business Days between the trade date and the effective or settlement date of the instrument.  This field is now deprecated and not picked up in schedule generation or adjustment to bond accrual start date. Defaulted to 0 if not set.")
    reset_days: Optional[StrictInt] = Field(None, alias="resetDays", description="The number of Good Business Days between determination and payment of reset. Defaulted to 0 if not set.")
    leap_days_included: Optional[StrictBool] = Field(None, alias="leapDaysIncluded", description="If this flag is set to true, the 29th of February is included in the date schedule when the business roll convention is applied.  If this flag is set to false, the business roll convention ignores February 29 for date schedules, cash flow payments etc.  This flag defaults to true if not specified, i.e., leap days are included in a date schedule generation.")
    accrual_date_adjustment: Optional[constr(strict=True, max_length=50, min_length=0)] = Field(None, alias="accrualDateAdjustment", description="Indicates if the accrual dates are adjusted to the payment dates. The default value is 'Adjusted'.    Supported string (enumeration) values are: [Adjusted, Unadjusted].")
    business_day_convention: Optional[StrictStr] = Field(None, alias="businessDayConvention", description="When generating a set of dates, what convention should be used for adjusting dates that coincide with a non-business day.    Supported string (enumeration) values are: [NoAdjustment, None, Previous, P, Following, F, ModifiedPrevious, MP, ModifiedFollowing, MF, HalfMonthModifiedFollowing, Nearest].")
    scope: Optional[constr(strict=True, max_length=256, min_length=1)] = Field(None, description="The scope used when updating or inserting the convention.")
    code: Optional[constr(strict=True, max_length=256, min_length=1)] = Field(None, description="The code of the convention.")
    __properties = ["currency", "paymentFrequency", "dayCountConvention", "rollConvention", "paymentCalendars", "resetCalendars", "settleDays", "resetDays", "leapDaysIncluded", "accrualDateAdjustment", "businessDayConvention", "scope", "code"]

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
    def from_json(cls, json_str: str) -> FlowConventions:
        """Create an instance of FlowConventions from a JSON string"""
        return cls.from_dict(json.loads(json_str))

    def to_dict(self):
        """Returns the dictionary representation of the model using alias"""
        _dict = self.dict(by_alias=True,
                          exclude={
                          },
                          exclude_none=True)
        # set to None if leap_days_included (nullable) is None
        # and __fields_set__ contains the field
        if self.leap_days_included is None and "leap_days_included" in self.__fields_set__:
            _dict['leapDaysIncluded'] = None

        # set to None if accrual_date_adjustment (nullable) is None
        # and __fields_set__ contains the field
        if self.accrual_date_adjustment is None and "accrual_date_adjustment" in self.__fields_set__:
            _dict['accrualDateAdjustment'] = None

        # set to None if business_day_convention (nullable) is None
        # and __fields_set__ contains the field
        if self.business_day_convention is None and "business_day_convention" in self.__fields_set__:
            _dict['businessDayConvention'] = None

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
    def from_dict(cls, obj: dict) -> FlowConventions:
        """Create an instance of FlowConventions from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return FlowConventions.parse_obj(obj)

        _obj = FlowConventions.parse_obj({
            "currency": obj.get("currency"),
            "payment_frequency": obj.get("paymentFrequency"),
            "day_count_convention": obj.get("dayCountConvention"),
            "roll_convention": obj.get("rollConvention"),
            "payment_calendars": obj.get("paymentCalendars"),
            "reset_calendars": obj.get("resetCalendars"),
            "settle_days": obj.get("settleDays"),
            "reset_days": obj.get("resetDays"),
            "leap_days_included": obj.get("leapDaysIncluded"),
            "accrual_date_adjustment": obj.get("accrualDateAdjustment"),
            "business_day_convention": obj.get("businessDayConvention"),
            "scope": obj.get("scope"),
            "code": obj.get("code")
        })
        return _obj
