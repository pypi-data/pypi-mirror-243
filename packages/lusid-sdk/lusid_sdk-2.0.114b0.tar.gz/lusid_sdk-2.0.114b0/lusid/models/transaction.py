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
from typing import Any, Dict, Optional, Union
from pydantic import BaseModel, Field, StrictFloat, StrictInt, StrictStr, constr, validator
from lusid.models.currency_and_amount import CurrencyAndAmount
from lusid.models.custodian_account import CustodianAccount
from lusid.models.otc_confirmation import OtcConfirmation
from lusid.models.perpetual_property import PerpetualProperty
from lusid.models.resource_id import ResourceId
from lusid.models.transaction_price import TransactionPrice

class Transaction(BaseModel):
    """
    A list of transactions.  # noqa: E501
    """
    transaction_id: constr(strict=True, min_length=1) = Field(..., alias="transactionId", description="The unique identifier for the transaction.")
    type: constr(strict=True, min_length=1) = Field(..., description="The type of the transaction e.g. 'Buy', 'Sell'. The transaction type should have been pre-configured via the System Configuration API endpoint.")
    instrument_identifiers: Optional[Dict[str, StrictStr]] = Field(None, alias="instrumentIdentifiers", description="A set of instrument identifiers that can resolve the transaction to a unique instrument.")
    instrument_scope: Optional[StrictStr] = Field(None, alias="instrumentScope", description="The scope in which the transaction's instrument lies.")
    instrument_uid: constr(strict=True, min_length=1) = Field(..., alias="instrumentUid", description="The unique Lusid Instrument Id (LUID) of the instrument that the transaction is in.")
    transaction_date: datetime = Field(..., alias="transactionDate", description="The date of the transaction.")
    settlement_date: datetime = Field(..., alias="settlementDate", description="The settlement date of the transaction.")
    units: Union[StrictFloat, StrictInt] = Field(..., description="The number of units transacted in the associated instrument.")
    transaction_price: Optional[TransactionPrice] = Field(None, alias="transactionPrice")
    total_consideration: CurrencyAndAmount = Field(..., alias="totalConsideration")
    exchange_rate: Optional[Union[StrictFloat, StrictInt]] = Field(None, alias="exchangeRate", description="The exchange rate between the transaction and settlement currency (settlement currency being represented by the TotalConsideration.Currency). For example if the transaction currency is in USD and the settlement currency is in GBP this this the USD/GBP rate.")
    transaction_currency: Optional[StrictStr] = Field(None, alias="transactionCurrency", description="The transaction currency.")
    properties: Optional[Dict[str, PerpetualProperty]] = Field(None, description="Set of unique transaction properties and associated values to stored with the transaction. Each property will be from the 'Transaction' domain.")
    counterparty_id: Optional[StrictStr] = Field(None, alias="counterpartyId", description="The identifier for the counterparty of the transaction.")
    source: Optional[StrictStr] = Field(None, description="The source of the transaction. This is used to look up the appropriate transaction group set in the transaction type configuration.")
    entry_date_time: Optional[datetime] = Field(None, alias="entryDateTime", description="The asAt datetime that the transaction was added to LUSID.")
    otc_confirmation: Optional[OtcConfirmation] = Field(None, alias="otcConfirmation")
    transaction_status: Optional[StrictStr] = Field(None, alias="transactionStatus", description="The status of the transaction. The available values are: Active, Amended, Cancelled")
    cancel_date_time: Optional[datetime] = Field(None, alias="cancelDateTime", description="If the transaction has been cancelled, the asAt datetime that the transaction was cancelled.")
    order_id: Optional[ResourceId] = Field(None, alias="orderId")
    allocation_id: Optional[ResourceId] = Field(None, alias="allocationId")
    custodian_account: Optional[CustodianAccount] = Field(None, alias="custodianAccount")
    __properties = ["transactionId", "type", "instrumentIdentifiers", "instrumentScope", "instrumentUid", "transactionDate", "settlementDate", "units", "transactionPrice", "totalConsideration", "exchangeRate", "transactionCurrency", "properties", "counterpartyId", "source", "entryDateTime", "otcConfirmation", "transactionStatus", "cancelDateTime", "orderId", "allocationId", "custodianAccount"]

    @validator('transaction_status')
    def transaction_status_validate_enum(cls, value):
        """Validates the enum"""
        if value is None:
            return value

        if value not in ('Active', 'Amended', 'Cancelled'):
            raise ValueError("must be one of enum values ('Active', 'Amended', 'Cancelled')")
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
    def from_json(cls, json_str: str) -> Transaction:
        """Create an instance of Transaction from a JSON string"""
        return cls.from_dict(json.loads(json_str))

    def to_dict(self):
        """Returns the dictionary representation of the model using alias"""
        _dict = self.dict(by_alias=True,
                          exclude={
                          },
                          exclude_none=True)
        # override the default output from pydantic by calling `to_dict()` of transaction_price
        if self.transaction_price:
            _dict['transactionPrice'] = self.transaction_price.to_dict()
        # override the default output from pydantic by calling `to_dict()` of total_consideration
        if self.total_consideration:
            _dict['totalConsideration'] = self.total_consideration.to_dict()
        # override the default output from pydantic by calling `to_dict()` of each value in properties (dict)
        _field_dict = {}
        if self.properties:
            for _key in self.properties:
                if self.properties[_key]:
                    _field_dict[_key] = self.properties[_key].to_dict()
            _dict['properties'] = _field_dict
        # override the default output from pydantic by calling `to_dict()` of otc_confirmation
        if self.otc_confirmation:
            _dict['otcConfirmation'] = self.otc_confirmation.to_dict()
        # override the default output from pydantic by calling `to_dict()` of order_id
        if self.order_id:
            _dict['orderId'] = self.order_id.to_dict()
        # override the default output from pydantic by calling `to_dict()` of allocation_id
        if self.allocation_id:
            _dict['allocationId'] = self.allocation_id.to_dict()
        # override the default output from pydantic by calling `to_dict()` of custodian_account
        if self.custodian_account:
            _dict['custodianAccount'] = self.custodian_account.to_dict()
        # set to None if instrument_identifiers (nullable) is None
        # and __fields_set__ contains the field
        if self.instrument_identifiers is None and "instrument_identifiers" in self.__fields_set__:
            _dict['instrumentIdentifiers'] = None

        # set to None if instrument_scope (nullable) is None
        # and __fields_set__ contains the field
        if self.instrument_scope is None and "instrument_scope" in self.__fields_set__:
            _dict['instrumentScope'] = None

        # set to None if exchange_rate (nullable) is None
        # and __fields_set__ contains the field
        if self.exchange_rate is None and "exchange_rate" in self.__fields_set__:
            _dict['exchangeRate'] = None

        # set to None if transaction_currency (nullable) is None
        # and __fields_set__ contains the field
        if self.transaction_currency is None and "transaction_currency" in self.__fields_set__:
            _dict['transactionCurrency'] = None

        # set to None if properties (nullable) is None
        # and __fields_set__ contains the field
        if self.properties is None and "properties" in self.__fields_set__:
            _dict['properties'] = None

        # set to None if counterparty_id (nullable) is None
        # and __fields_set__ contains the field
        if self.counterparty_id is None and "counterparty_id" in self.__fields_set__:
            _dict['counterpartyId'] = None

        # set to None if source (nullable) is None
        # and __fields_set__ contains the field
        if self.source is None and "source" in self.__fields_set__:
            _dict['source'] = None

        # set to None if cancel_date_time (nullable) is None
        # and __fields_set__ contains the field
        if self.cancel_date_time is None and "cancel_date_time" in self.__fields_set__:
            _dict['cancelDateTime'] = None

        return _dict

    @classmethod
    def from_dict(cls, obj: dict) -> Transaction:
        """Create an instance of Transaction from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return Transaction.parse_obj(obj)

        _obj = Transaction.parse_obj({
            "transaction_id": obj.get("transactionId"),
            "type": obj.get("type"),
            "instrument_identifiers": obj.get("instrumentIdentifiers"),
            "instrument_scope": obj.get("instrumentScope"),
            "instrument_uid": obj.get("instrumentUid"),
            "transaction_date": obj.get("transactionDate"),
            "settlement_date": obj.get("settlementDate"),
            "units": obj.get("units"),
            "transaction_price": TransactionPrice.from_dict(obj.get("transactionPrice")) if obj.get("transactionPrice") is not None else None,
            "total_consideration": CurrencyAndAmount.from_dict(obj.get("totalConsideration")) if obj.get("totalConsideration") is not None else None,
            "exchange_rate": obj.get("exchangeRate"),
            "transaction_currency": obj.get("transactionCurrency"),
            "properties": dict(
                (_k, PerpetualProperty.from_dict(_v))
                for _k, _v in obj.get("properties").items()
            )
            if obj.get("properties") is not None
            else None,
            "counterparty_id": obj.get("counterpartyId"),
            "source": obj.get("source"),
            "entry_date_time": obj.get("entryDateTime"),
            "otc_confirmation": OtcConfirmation.from_dict(obj.get("otcConfirmation")) if obj.get("otcConfirmation") is not None else None,
            "transaction_status": obj.get("transactionStatus"),
            "cancel_date_time": obj.get("cancelDateTime"),
            "order_id": ResourceId.from_dict(obj.get("orderId")) if obj.get("orderId") is not None else None,
            "allocation_id": ResourceId.from_dict(obj.get("allocationId")) if obj.get("allocationId") is not None else None,
            "custodian_account": CustodianAccount.from_dict(obj.get("custodianAccount")) if obj.get("custodianAccount") is not None else None
        })
        return _obj
