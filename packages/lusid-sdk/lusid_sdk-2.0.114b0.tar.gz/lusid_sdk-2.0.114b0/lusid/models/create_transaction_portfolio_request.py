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
from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field, StrictStr, conlist, constr, validator
from lusid.models.model_property import ModelProperty
from lusid.models.resource_id import ResourceId

class CreateTransactionPortfolioRequest(BaseModel):
    """
    CreateTransactionPortfolioRequest
    """
    display_name: constr(strict=True, min_length=1) = Field(..., alias="displayName", description="The name of the transaction portfolio.")
    description: Optional[StrictStr] = Field(None, description="A description for the transaction portfolio.")
    code: StrictStr = Field(..., description="The code of the transaction portfolio. Together with the scope this uniquely identifies the transaction portfolio.")
    created: Optional[datetime] = Field(None, description="The effective datetime at which to create the transaction portfolio. No transactions can be added to the transaction portfolio before this date. Defaults to the current LUSID system datetime if not specified.")
    base_currency: StrictStr = Field(..., alias="baseCurrency", description="The base currency of the transaction portfolio in ISO 4217 currency code format.")
    corporate_action_source_id: Optional[ResourceId] = Field(None, alias="corporateActionSourceId")
    accounting_method: Optional[StrictStr] = Field(None, alias="accountingMethod", description=". The available values are: Default, AverageCost, FirstInFirstOut, LastInFirstOut, HighestCostFirst, LowestCostFirst")
    sub_holding_keys: Optional[conlist(StrictStr, max_items=100)] = Field(None, alias="subHoldingKeys", description="A set of unique transaction properties to group the transaction portfolio's holdings by, perhaps for strategy tagging. Each property must be from the 'Transaction' domain and identified by a key in the format {domain}/{scope}/{code}, for example 'Transaction/strategies/quantsignal'. See https://support.lusid.com/knowledgebase/article/KA-01879/en-us for more information.")
    properties: Optional[Dict[str, ModelProperty]] = Field(None, description="A set of unique portfolio properties to add custom data to the transaction portfolio. Each property must be from the 'Portfolio' domain and identified by a key in the format {domain}/{scope}/{code}, for example 'Portfolio/Manager/Id'. Note these properties must be pre-defined.")
    instrument_scopes: Optional[conlist(StrictStr, max_items=1)] = Field(None, alias="instrumentScopes", description="The resolution strategy used to resolve instruments of transactions/holdings upserted to this portfolio.")
    amortisation_method: Optional[StrictStr] = Field(None, alias="amortisationMethod", description="The amortisation method the portfolio is using in the calculation. This can be 'NoAmortisation', 'StraightLine' or 'EffectiveYield'.")
    transaction_type_scope: Optional[constr(strict=True, max_length=64, min_length=1)] = Field(None, alias="transactionTypeScope", description="The scope of the transaction types.")
    cash_gain_loss_calculation_date: Optional[StrictStr] = Field(None, alias="cashGainLossCalculationDate", description="The option when the Cash Gain Loss to be calulated, TransactionDate/SettlementDate. Defaults to SettlementDate.")
    __properties = ["displayName", "description", "code", "created", "baseCurrency", "corporateActionSourceId", "accountingMethod", "subHoldingKeys", "properties", "instrumentScopes", "amortisationMethod", "transactionTypeScope", "cashGainLossCalculationDate"]

    @validator('accounting_method')
    def accounting_method_validate_enum(cls, value):
        """Validates the enum"""
        if value is None:
            return value

        if value not in ('Default', 'AverageCost', 'FirstInFirstOut', 'LastInFirstOut', 'HighestCostFirst', 'LowestCostFirst'):
            raise ValueError("must be one of enum values ('Default', 'AverageCost', 'FirstInFirstOut', 'LastInFirstOut', 'HighestCostFirst', 'LowestCostFirst')")
        return value

    @validator('transaction_type_scope')
    def transaction_type_scope_validate_regular_expression(cls, value):
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
    def from_json(cls, json_str: str) -> CreateTransactionPortfolioRequest:
        """Create an instance of CreateTransactionPortfolioRequest from a JSON string"""
        return cls.from_dict(json.loads(json_str))

    def to_dict(self):
        """Returns the dictionary representation of the model using alias"""
        _dict = self.dict(by_alias=True,
                          exclude={
                          },
                          exclude_none=True)
        # override the default output from pydantic by calling `to_dict()` of corporate_action_source_id
        if self.corporate_action_source_id:
            _dict['corporateActionSourceId'] = self.corporate_action_source_id.to_dict()
        # override the default output from pydantic by calling `to_dict()` of each value in properties (dict)
        _field_dict = {}
        if self.properties:
            for _key in self.properties:
                if self.properties[_key]:
                    _field_dict[_key] = self.properties[_key].to_dict()
            _dict['properties'] = _field_dict
        # set to None if description (nullable) is None
        # and __fields_set__ contains the field
        if self.description is None and "description" in self.__fields_set__:
            _dict['description'] = None

        # set to None if created (nullable) is None
        # and __fields_set__ contains the field
        if self.created is None and "created" in self.__fields_set__:
            _dict['created'] = None

        # set to None if sub_holding_keys (nullable) is None
        # and __fields_set__ contains the field
        if self.sub_holding_keys is None and "sub_holding_keys" in self.__fields_set__:
            _dict['subHoldingKeys'] = None

        # set to None if properties (nullable) is None
        # and __fields_set__ contains the field
        if self.properties is None and "properties" in self.__fields_set__:
            _dict['properties'] = None

        # set to None if instrument_scopes (nullable) is None
        # and __fields_set__ contains the field
        if self.instrument_scopes is None and "instrument_scopes" in self.__fields_set__:
            _dict['instrumentScopes'] = None

        # set to None if amortisation_method (nullable) is None
        # and __fields_set__ contains the field
        if self.amortisation_method is None and "amortisation_method" in self.__fields_set__:
            _dict['amortisationMethod'] = None

        # set to None if transaction_type_scope (nullable) is None
        # and __fields_set__ contains the field
        if self.transaction_type_scope is None and "transaction_type_scope" in self.__fields_set__:
            _dict['transactionTypeScope'] = None

        # set to None if cash_gain_loss_calculation_date (nullable) is None
        # and __fields_set__ contains the field
        if self.cash_gain_loss_calculation_date is None and "cash_gain_loss_calculation_date" in self.__fields_set__:
            _dict['cashGainLossCalculationDate'] = None

        return _dict

    @classmethod
    def from_dict(cls, obj: dict) -> CreateTransactionPortfolioRequest:
        """Create an instance of CreateTransactionPortfolioRequest from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return CreateTransactionPortfolioRequest.parse_obj(obj)

        _obj = CreateTransactionPortfolioRequest.parse_obj({
            "display_name": obj.get("displayName"),
            "description": obj.get("description"),
            "code": obj.get("code"),
            "created": obj.get("created"),
            "base_currency": obj.get("baseCurrency"),
            "corporate_action_source_id": ResourceId.from_dict(obj.get("corporateActionSourceId")) if obj.get("corporateActionSourceId") is not None else None,
            "accounting_method": obj.get("accountingMethod"),
            "sub_holding_keys": obj.get("subHoldingKeys"),
            "properties": dict(
                (_k, ModelProperty.from_dict(_v))
                for _k, _v in obj.get("properties").items()
            )
            if obj.get("properties") is not None
            else None,
            "instrument_scopes": obj.get("instrumentScopes"),
            "amortisation_method": obj.get("amortisationMethod"),
            "transaction_type_scope": obj.get("transactionTypeScope"),
            "cash_gain_loss_calculation_date": obj.get("cashGainLossCalculationDate")
        })
        return _obj
