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
from pydantic import BaseModel, Field, conlist
from lusid.models.corporate_action_transition_component_request import CorporateActionTransitionComponentRequest

class CorporateActionTransitionRequest(BaseModel):
    """
    A 'transition' within a corporate action, representing a set of output movements paired to a single input position  # noqa: E501
    """
    input_transition: Optional[CorporateActionTransitionComponentRequest] = Field(None, alias="inputTransition")
    output_transitions: Optional[conlist(CorporateActionTransitionComponentRequest)] = Field(None, alias="outputTransitions")
    __properties = ["inputTransition", "outputTransitions"]

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
    def from_json(cls, json_str: str) -> CorporateActionTransitionRequest:
        """Create an instance of CorporateActionTransitionRequest from a JSON string"""
        return cls.from_dict(json.loads(json_str))

    def to_dict(self):
        """Returns the dictionary representation of the model using alias"""
        _dict = self.dict(by_alias=True,
                          exclude={
                          },
                          exclude_none=True)
        # override the default output from pydantic by calling `to_dict()` of input_transition
        if self.input_transition:
            _dict['inputTransition'] = self.input_transition.to_dict()
        # override the default output from pydantic by calling `to_dict()` of each item in output_transitions (list)
        _items = []
        if self.output_transitions:
            for _item in self.output_transitions:
                if _item:
                    _items.append(_item.to_dict())
            _dict['outputTransitions'] = _items
        # set to None if output_transitions (nullable) is None
        # and __fields_set__ contains the field
        if self.output_transitions is None and "output_transitions" in self.__fields_set__:
            _dict['outputTransitions'] = None

        return _dict

    @classmethod
    def from_dict(cls, obj: dict) -> CorporateActionTransitionRequest:
        """Create an instance of CorporateActionTransitionRequest from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return CorporateActionTransitionRequest.parse_obj(obj)

        _obj = CorporateActionTransitionRequest.parse_obj({
            "input_transition": CorporateActionTransitionComponentRequest.from_dict(obj.get("inputTransition")) if obj.get("inputTransition") is not None else None,
            "output_transitions": [CorporateActionTransitionComponentRequest.from_dict(_item) for _item in obj.get("outputTransitions")] if obj.get("outputTransitions") is not None else None
        })
        return _obj
