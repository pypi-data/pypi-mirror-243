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
from pydantic import BaseModel, Field
from lusid.models.resource_id import ResourceId

class OtcConfirmation(BaseModel):
    """
    For the storage of any information pertinent to the confirmation of an OTC trade. e.g the Counterparty Agreement Code  # noqa: E501
    """
    counterparty_agreement_id: Optional[ResourceId] = Field(None, alias="counterpartyAgreementId")
    __properties = ["counterpartyAgreementId"]

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
    def from_json(cls, json_str: str) -> OtcConfirmation:
        """Create an instance of OtcConfirmation from a JSON string"""
        return cls.from_dict(json.loads(json_str))

    def to_dict(self):
        """Returns the dictionary representation of the model using alias"""
        _dict = self.dict(by_alias=True,
                          exclude={
                          },
                          exclude_none=True)
        # override the default output from pydantic by calling `to_dict()` of counterparty_agreement_id
        if self.counterparty_agreement_id:
            _dict['counterpartyAgreementId'] = self.counterparty_agreement_id.to_dict()
        return _dict

    @classmethod
    def from_dict(cls, obj: dict) -> OtcConfirmation:
        """Create an instance of OtcConfirmation from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return OtcConfirmation.parse_obj(obj)

        _obj = OtcConfirmation.parse_obj({
            "counterparty_agreement_id": ResourceId.from_dict(obj.get("counterpartyAgreementId")) if obj.get("counterpartyAgreementId") is not None else None
        })
        return _obj
