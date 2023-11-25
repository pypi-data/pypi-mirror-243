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
from pydantic import BaseModel, Field, StrictStr, constr

class CreateRelationDefinitionRequest(BaseModel):
    """
    CreateRelationDefinitionRequest
    """
    scope: StrictStr = Field(..., description="The scope that the relation exists in.")
    code: StrictStr = Field(..., description="The code of the relation. Together with the scope this uniquely defines the relation.")
    source_entity_domain: constr(strict=True, min_length=1) = Field(..., alias="sourceEntityDomain", description="The entity domain of the source entity object must be, allowed values are \"Portfolio\" and \"Person\"")
    target_entity_domain: constr(strict=True, min_length=1) = Field(..., alias="targetEntityDomain", description="The entity domain of the target entity object must be, allowed values are \"Portfolio\" and \"Person\"")
    display_name: constr(strict=True, min_length=1) = Field(..., alias="displayName", description="The display name of the relation.")
    outward_description: constr(strict=True, min_length=1) = Field(..., alias="outwardDescription", description="The description to relate source entity object and target entity object.")
    inward_description: constr(strict=True, min_length=1) = Field(..., alias="inwardDescription", description="The description to relate target entity object and source entity object.")
    life_time: Optional[StrictStr] = Field(None, alias="lifeTime", description="Describes how the relations can change over time, allowed values are \"Perpetual\" and \"TimeVariant\"")
    constraint_style: Optional[StrictStr] = Field(None, alias="constraintStyle", description="Describes the uniqueness and cardinality for relations with a specific source entity object and relations under this definition. Allowed values are \"Property\" and \"Collection\", defaults to \"Collection\" if not specified.")
    __properties = ["scope", "code", "sourceEntityDomain", "targetEntityDomain", "displayName", "outwardDescription", "inwardDescription", "lifeTime", "constraintStyle"]

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
    def from_json(cls, json_str: str) -> CreateRelationDefinitionRequest:
        """Create an instance of CreateRelationDefinitionRequest from a JSON string"""
        return cls.from_dict(json.loads(json_str))

    def to_dict(self):
        """Returns the dictionary representation of the model using alias"""
        _dict = self.dict(by_alias=True,
                          exclude={
                          },
                          exclude_none=True)
        # set to None if life_time (nullable) is None
        # and __fields_set__ contains the field
        if self.life_time is None and "life_time" in self.__fields_set__:
            _dict['lifeTime'] = None

        # set to None if constraint_style (nullable) is None
        # and __fields_set__ contains the field
        if self.constraint_style is None and "constraint_style" in self.__fields_set__:
            _dict['constraintStyle'] = None

        return _dict

    @classmethod
    def from_dict(cls, obj: dict) -> CreateRelationDefinitionRequest:
        """Create an instance of CreateRelationDefinitionRequest from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return CreateRelationDefinitionRequest.parse_obj(obj)

        _obj = CreateRelationDefinitionRequest.parse_obj({
            "scope": obj.get("scope"),
            "code": obj.get("code"),
            "source_entity_domain": obj.get("sourceEntityDomain"),
            "target_entity_domain": obj.get("targetEntityDomain"),
            "display_name": obj.get("displayName"),
            "outward_description": obj.get("outwardDescription"),
            "inward_description": obj.get("inwardDescription"),
            "life_time": obj.get("lifeTime"),
            "constraint_style": obj.get("constraintStyle")
        })
        return _obj
