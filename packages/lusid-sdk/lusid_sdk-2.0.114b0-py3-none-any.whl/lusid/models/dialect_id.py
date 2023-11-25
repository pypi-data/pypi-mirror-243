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


from typing import Any, Dict
from pydantic import BaseModel, Field, constr, validator

class DialectId(BaseModel):
    """
    Unique identifier of a given Dialect  # noqa: E501
    """
    scope: constr(strict=True, max_length=64, min_length=1) = Field(..., description="The Scope of the dialect.")
    vendor: constr(strict=True, max_length=64, min_length=1) = Field(..., description="The vendor of the dialect, the entity that created it. e.g. ISDA, FINBOURNE.")
    source_system: constr(strict=True, max_length=64, min_length=1) = Field(..., alias="sourceSystem", description="The source system of the dialect, the system that understands it. e.g. LUSID, QuantLib.")
    version: constr(strict=True, max_length=30, min_length=1) = Field(..., description="The semantic version of the dialect: MAJOR.MINOR.PATCH.")
    serialisation_format: constr(strict=True, min_length=1) = Field(..., alias="serialisationFormat", description="The serialisation format of a document in this dialect. e.g. JSON, XML.")
    entity_type: constr(strict=True, min_length=1) = Field(..., alias="entityType", description="The type of entity this dialect describes e.g. Instrument.")
    __properties = ["scope", "vendor", "sourceSystem", "version", "serialisationFormat", "entityType"]

    @validator('scope')
    def scope_validate_regular_expression(cls, value):
        """Validates the regular expression"""
        if not re.match(r"^[a-zA-Z0-9\-_]+$", value):
            raise ValueError(r"must validate the regular expression /^[a-zA-Z0-9\-_]+$/")
        return value

    @validator('vendor')
    def vendor_validate_regular_expression(cls, value):
        """Validates the regular expression"""
        if not re.match(r"^[a-zA-Z0-9\-_]+$", value):
            raise ValueError(r"must validate the regular expression /^[a-zA-Z0-9\-_]+$/")
        return value

    @validator('source_system')
    def source_system_validate_regular_expression(cls, value):
        """Validates the regular expression"""
        if not re.match(r"^[a-zA-Z0-9\-_]+$", value):
            raise ValueError(r"must validate the regular expression /^[a-zA-Z0-9\-_]+$/")
        return value

    @validator('version')
    def version_validate_regular_expression(cls, value):
        """Validates the regular expression"""
        if not re.match(r"^(0|[1-9]\d*)\.(0|[1-9]\d*)\.(0|[1-9]\d*)$", value):
            raise ValueError(r"must validate the regular expression /^(0|[1-9]\d*)\.(0|[1-9]\d*)\.(0|[1-9]\d*)$/")
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
    def from_json(cls, json_str: str) -> DialectId:
        """Create an instance of DialectId from a JSON string"""
        return cls.from_dict(json.loads(json_str))

    def to_dict(self):
        """Returns the dictionary representation of the model using alias"""
        _dict = self.dict(by_alias=True,
                          exclude={
                          },
                          exclude_none=True)
        return _dict

    @classmethod
    def from_dict(cls, obj: dict) -> DialectId:
        """Create an instance of DialectId from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return DialectId.parse_obj(obj)

        _obj = DialectId.parse_obj({
            "scope": obj.get("scope"),
            "vendor": obj.get("vendor"),
            "source_system": obj.get("sourceSystem"),
            "version": obj.get("version"),
            "serialisation_format": obj.get("serialisationFormat"),
            "entity_type": obj.get("entityType")
        })
        return _obj
