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
from pydantic import BaseModel, Field, StrictInt, StrictStr, conlist, constr, validator
from lusid.models.perpetual_property import PerpetualProperty
from lusid.models.transaction_property_mapping_request import TransactionPropertyMappingRequest

class TransactionConfigurationMovementDataRequest(BaseModel):
    """
    TransactionConfigurationMovementDataRequest
    """
    movement_types: StrictStr = Field(..., alias="movementTypes", description=". The available values are: Settlement, Traded, StockMovement, FutureCash, Commitment, Receivable, CashSettlement, CashForward, CashCommitment, CashReceivable, Accrual, CashAccrual, ForwardFx, CashFxForward, UnsettledCashTypes, Carry, CarryAsPnl, VariationMargin")
    side: constr(strict=True, min_length=1) = Field(..., description="The movement side")
    direction: StrictInt = Field(..., description="The movement direction")
    properties: Optional[Dict[str, PerpetualProperty]] = Field(None, description="The properties associated with the underlying Movement.")
    mappings: Optional[conlist(TransactionPropertyMappingRequest)] = Field(None, description="This allows you to map a transaction property to a property on the underlying holding.")
    name: Optional[StrictStr] = Field(None, description="The movement name (optional)")
    movement_options: Optional[conlist(StrictStr)] = Field(None, alias="movementOptions", description="Allows extra specifications for the movement. The only option currently available is 'DirectAdjustment'. A movement type of 'StockMovement' with an option of 'DirectAdjusment' will allow you to adjust the unitsof a holding without affecting its cost base. You will, therefore, be able to reflect the impact of a stock split by loading a Transaction.")
    __properties = ["movementTypes", "side", "direction", "properties", "mappings", "name", "movementOptions"]

    @validator('movement_types')
    def movement_types_validate_enum(cls, value):
        """Validates the enum"""
        if value not in ('Settlement', 'Traded', 'StockMovement', 'FutureCash', 'Commitment', 'Receivable', 'CashSettlement', 'CashForward', 'CashCommitment', 'CashReceivable', 'Accrual', 'CashAccrual', 'ForwardFx', 'CashFxForward', 'UnsettledCashTypes', 'Carry', 'CarryAsPnl', 'VariationMargin'):
            raise ValueError("must be one of enum values ('Settlement', 'Traded', 'StockMovement', 'FutureCash', 'Commitment', 'Receivable', 'CashSettlement', 'CashForward', 'CashCommitment', 'CashReceivable', 'Accrual', 'CashAccrual', 'ForwardFx', 'CashFxForward', 'UnsettledCashTypes', 'Carry', 'CarryAsPnl', 'VariationMargin')")
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
    def from_json(cls, json_str: str) -> TransactionConfigurationMovementDataRequest:
        """Create an instance of TransactionConfigurationMovementDataRequest from a JSON string"""
        return cls.from_dict(json.loads(json_str))

    def to_dict(self):
        """Returns the dictionary representation of the model using alias"""
        _dict = self.dict(by_alias=True,
                          exclude={
                          },
                          exclude_none=True)
        # override the default output from pydantic by calling `to_dict()` of each value in properties (dict)
        _field_dict = {}
        if self.properties:
            for _key in self.properties:
                if self.properties[_key]:
                    _field_dict[_key] = self.properties[_key].to_dict()
            _dict['properties'] = _field_dict
        # override the default output from pydantic by calling `to_dict()` of each item in mappings (list)
        _items = []
        if self.mappings:
            for _item in self.mappings:
                if _item:
                    _items.append(_item.to_dict())
            _dict['mappings'] = _items
        # set to None if properties (nullable) is None
        # and __fields_set__ contains the field
        if self.properties is None and "properties" in self.__fields_set__:
            _dict['properties'] = None

        # set to None if mappings (nullable) is None
        # and __fields_set__ contains the field
        if self.mappings is None and "mappings" in self.__fields_set__:
            _dict['mappings'] = None

        # set to None if name (nullable) is None
        # and __fields_set__ contains the field
        if self.name is None and "name" in self.__fields_set__:
            _dict['name'] = None

        # set to None if movement_options (nullable) is None
        # and __fields_set__ contains the field
        if self.movement_options is None and "movement_options" in self.__fields_set__:
            _dict['movementOptions'] = None

        return _dict

    @classmethod
    def from_dict(cls, obj: dict) -> TransactionConfigurationMovementDataRequest:
        """Create an instance of TransactionConfigurationMovementDataRequest from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return TransactionConfigurationMovementDataRequest.parse_obj(obj)

        _obj = TransactionConfigurationMovementDataRequest.parse_obj({
            "movement_types": obj.get("movementTypes"),
            "side": obj.get("side"),
            "direction": obj.get("direction"),
            "properties": dict(
                (_k, PerpetualProperty.from_dict(_v))
                for _k, _v in obj.get("properties").items()
            )
            if obj.get("properties") is not None
            else None,
            "mappings": [TransactionPropertyMappingRequest.from_dict(_item) for _item in obj.get("mappings")] if obj.get("mappings") is not None else None,
            "name": obj.get("name"),
            "movement_options": obj.get("movementOptions")
        })
        return _obj
