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
from pydantic import BaseModel, Field, StrictBool, StrictStr, conlist, validator
from lusid.models.link import Link
from lusid.models.model_property import ModelProperty
from lusid.models.resource_id import ResourceId
from lusid.models.version import Version

class PropertyDefinition(BaseModel):
    """
    A list of property definitions.  # noqa: E501
    """
    href: Optional[StrictStr] = Field(None, description="The specific Uniform Resource Identifier (URI) for this resource at the requested effective and asAt datetime.")
    key: Optional[StrictStr] = Field(None, description="The property key which uniquely identifies the property. The format for the property key is {domain}/{scope}/{code}, e.g. 'Portfolio/Manager/Id'.")
    value_type: Optional[StrictStr] = Field(None, alias="valueType", description="The type of values that can be associated with this property. This is defined by the property's data type. The available values are: String, Int, Decimal, DateTime, Boolean, Map, List, PropertyArray, Percentage, Code, Id, Uri, CurrencyAndAmount, TradePrice, Currency, MetricValue, ResourceId, ResultValue, CutLocalTime, DateOrCutLabel, UnindexedText")
    display_name: Optional[StrictStr] = Field(None, alias="displayName", description="The display name of the property.")
    data_type_id: Optional[ResourceId] = Field(None, alias="dataTypeId")
    type: Optional[StrictStr] = Field(None, description="The type of the property. The available values are: Label, Metric, Information")
    unit_schema: Optional[StrictStr] = Field(None, alias="unitSchema", description="The units that can be associated with the property's values. This is defined by the property's data type. The available values are: NoUnits, Basic, Iso4217Currency")
    domain: Optional[StrictStr] = Field(None, description="The domain that the property exists in. The available values are: NotDefined, Transaction, Portfolio, Holding, ReferenceHolding, TransactionConfiguration, Instrument, CutLabelDefinition, Analytic, PortfolioGroup, Person, AccessMetadata, Order, UnitResult, MarketData, ConfigurationRecipe, Allocation, Calendar, LegalEntity, Placement, Execution, Block, Participation, Package, OrderInstruction, NextBestAction, CustomEntity, InstrumentEvent, Account, ChartOfAccounts, CustodianAccount, Abor, AborConfiguration, Reconciliation, PropertyDefinition, Compliance, DiaryEntry")
    scope: Optional[StrictStr] = Field(None, description="The scope that the property exists in.")
    code: Optional[StrictStr] = Field(None, description="The code of the property. Together with the domain and scope this uniquely identifies the property.")
    value_required: Optional[StrictBool] = Field(None, alias="valueRequired", description="This field is not implemented and should be disregarded.")
    life_time: Optional[StrictStr] = Field(None, alias="lifeTime", description="Describes how the property's values can change over time. The available values are: Perpetual, TimeVariant")
    constraint_style: Optional[StrictStr] = Field(None, alias="constraintStyle", description="Describes the uniqueness and cardinality of the property for entity objects under the property domain specified in Key.")
    property_definition_type: Optional[StrictStr] = Field(None, alias="propertyDefinitionType", description="The definition type (DerivedDefinition or Definition). The available values are: ValueProperty, DerivedDefinition")
    property_description: Optional[StrictStr] = Field(None, alias="propertyDescription", description="A brief description of what a property of this property definition contains.")
    derivation_formula: Optional[StrictStr] = Field(None, alias="derivationFormula", description="The rule that defines how data is composed for a derived property.")
    properties: Optional[Dict[str, ModelProperty]] = Field(None, description="Set of unique property definition properties and associated values to store with the property definition. Each property must be from the 'PropertyDefinition' domain.")
    version: Optional[Version] = None
    links: Optional[conlist(Link)] = None
    __properties = ["href", "key", "valueType", "displayName", "dataTypeId", "type", "unitSchema", "domain", "scope", "code", "valueRequired", "lifeTime", "constraintStyle", "propertyDefinitionType", "propertyDescription", "derivationFormula", "properties", "version", "links"]

    @validator('value_type')
    def value_type_validate_enum(cls, value):
        """Validates the enum"""
        if value is None:
            return value

        if value not in ('String', 'Int', 'Decimal', 'DateTime', 'Boolean', 'Map', 'List', 'PropertyArray', 'Percentage', 'Code', 'Id', 'Uri', 'CurrencyAndAmount', 'TradePrice', 'Currency', 'MetricValue', 'ResourceId', 'ResultValue', 'CutLocalTime', 'DateOrCutLabel', 'UnindexedText'):
            raise ValueError("must be one of enum values ('String', 'Int', 'Decimal', 'DateTime', 'Boolean', 'Map', 'List', 'PropertyArray', 'Percentage', 'Code', 'Id', 'Uri', 'CurrencyAndAmount', 'TradePrice', 'Currency', 'MetricValue', 'ResourceId', 'ResultValue', 'CutLocalTime', 'DateOrCutLabel', 'UnindexedText')")
        return value

    @validator('type')
    def type_validate_enum(cls, value):
        """Validates the enum"""
        if value is None:
            return value

        if value not in ('Label', 'Metric', 'Information'):
            raise ValueError("must be one of enum values ('Label', 'Metric', 'Information')")
        return value

    @validator('unit_schema')
    def unit_schema_validate_enum(cls, value):
        """Validates the enum"""
        if value is None:
            return value

        if value not in ('NoUnits', 'Basic', 'Iso4217Currency'):
            raise ValueError("must be one of enum values ('NoUnits', 'Basic', 'Iso4217Currency')")
        return value

    @validator('domain')
    def domain_validate_enum(cls, value):
        """Validates the enum"""
        if value is None:
            return value

        if value not in ('NotDefined', 'Transaction', 'Portfolio', 'Holding', 'ReferenceHolding', 'TransactionConfiguration', 'Instrument', 'CutLabelDefinition', 'Analytic', 'PortfolioGroup', 'Person', 'AccessMetadata', 'Order', 'UnitResult', 'MarketData', 'ConfigurationRecipe', 'Allocation', 'Calendar', 'LegalEntity', 'Placement', 'Execution', 'Block', 'Participation', 'Package', 'OrderInstruction', 'NextBestAction', 'CustomEntity', 'InstrumentEvent', 'Account', 'ChartOfAccounts', 'CustodianAccount', 'Abor', 'AborConfiguration', 'Reconciliation', 'PropertyDefinition', 'Compliance', 'DiaryEntry'):
            raise ValueError("must be one of enum values ('NotDefined', 'Transaction', 'Portfolio', 'Holding', 'ReferenceHolding', 'TransactionConfiguration', 'Instrument', 'CutLabelDefinition', 'Analytic', 'PortfolioGroup', 'Person', 'AccessMetadata', 'Order', 'UnitResult', 'MarketData', 'ConfigurationRecipe', 'Allocation', 'Calendar', 'LegalEntity', 'Placement', 'Execution', 'Block', 'Participation', 'Package', 'OrderInstruction', 'NextBestAction', 'CustomEntity', 'InstrumentEvent', 'Account', 'ChartOfAccounts', 'CustodianAccount', 'Abor', 'AborConfiguration', 'Reconciliation', 'PropertyDefinition', 'Compliance', 'DiaryEntry')")
        return value

    @validator('life_time')
    def life_time_validate_enum(cls, value):
        """Validates the enum"""
        if value is None:
            return value

        if value not in ('Perpetual', 'TimeVariant'):
            raise ValueError("must be one of enum values ('Perpetual', 'TimeVariant')")
        return value

    @validator('property_definition_type')
    def property_definition_type_validate_enum(cls, value):
        """Validates the enum"""
        if value is None:
            return value

        if value not in ('ValueProperty', 'DerivedDefinition'):
            raise ValueError("must be one of enum values ('ValueProperty', 'DerivedDefinition')")
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
    def from_json(cls, json_str: str) -> PropertyDefinition:
        """Create an instance of PropertyDefinition from a JSON string"""
        return cls.from_dict(json.loads(json_str))

    def to_dict(self):
        """Returns the dictionary representation of the model using alias"""
        _dict = self.dict(by_alias=True,
                          exclude={
                            "scope",
                            "code",
                          },
                          exclude_none=True)
        # override the default output from pydantic by calling `to_dict()` of data_type_id
        if self.data_type_id:
            _dict['dataTypeId'] = self.data_type_id.to_dict()
        # override the default output from pydantic by calling `to_dict()` of each value in properties (dict)
        _field_dict = {}
        if self.properties:
            for _key in self.properties:
                if self.properties[_key]:
                    _field_dict[_key] = self.properties[_key].to_dict()
            _dict['properties'] = _field_dict
        # override the default output from pydantic by calling `to_dict()` of version
        if self.version:
            _dict['version'] = self.version.to_dict()
        # override the default output from pydantic by calling `to_dict()` of each item in links (list)
        _items = []
        if self.links:
            for _item in self.links:
                if _item:
                    _items.append(_item.to_dict())
            _dict['links'] = _items
        # set to None if href (nullable) is None
        # and __fields_set__ contains the field
        if self.href is None and "href" in self.__fields_set__:
            _dict['href'] = None

        # set to None if key (nullable) is None
        # and __fields_set__ contains the field
        if self.key is None and "key" in self.__fields_set__:
            _dict['key'] = None

        # set to None if display_name (nullable) is None
        # and __fields_set__ contains the field
        if self.display_name is None and "display_name" in self.__fields_set__:
            _dict['displayName'] = None

        # set to None if scope (nullable) is None
        # and __fields_set__ contains the field
        if self.scope is None and "scope" in self.__fields_set__:
            _dict['scope'] = None

        # set to None if code (nullable) is None
        # and __fields_set__ contains the field
        if self.code is None and "code" in self.__fields_set__:
            _dict['code'] = None

        # set to None if constraint_style (nullable) is None
        # and __fields_set__ contains the field
        if self.constraint_style is None and "constraint_style" in self.__fields_set__:
            _dict['constraintStyle'] = None

        # set to None if property_description (nullable) is None
        # and __fields_set__ contains the field
        if self.property_description is None and "property_description" in self.__fields_set__:
            _dict['propertyDescription'] = None

        # set to None if derivation_formula (nullable) is None
        # and __fields_set__ contains the field
        if self.derivation_formula is None and "derivation_formula" in self.__fields_set__:
            _dict['derivationFormula'] = None

        # set to None if properties (nullable) is None
        # and __fields_set__ contains the field
        if self.properties is None and "properties" in self.__fields_set__:
            _dict['properties'] = None

        # set to None if links (nullable) is None
        # and __fields_set__ contains the field
        if self.links is None and "links" in self.__fields_set__:
            _dict['links'] = None

        return _dict

    @classmethod
    def from_dict(cls, obj: dict) -> PropertyDefinition:
        """Create an instance of PropertyDefinition from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return PropertyDefinition.parse_obj(obj)

        _obj = PropertyDefinition.parse_obj({
            "href": obj.get("href"),
            "key": obj.get("key"),
            "value_type": obj.get("valueType"),
            "display_name": obj.get("displayName"),
            "data_type_id": ResourceId.from_dict(obj.get("dataTypeId")) if obj.get("dataTypeId") is not None else None,
            "type": obj.get("type"),
            "unit_schema": obj.get("unitSchema"),
            "domain": obj.get("domain"),
            "scope": obj.get("scope"),
            "code": obj.get("code"),
            "value_required": obj.get("valueRequired"),
            "life_time": obj.get("lifeTime"),
            "constraint_style": obj.get("constraintStyle"),
            "property_definition_type": obj.get("propertyDefinitionType"),
            "property_description": obj.get("propertyDescription"),
            "derivation_formula": obj.get("derivationFormula"),
            "properties": dict(
                (_k, ModelProperty.from_dict(_v))
                for _k, _v in obj.get("properties").items()
            )
            if obj.get("properties") is not None
            else None,
            "version": Version.from_dict(obj.get("version")) if obj.get("version") is not None else None,
            "links": [Link.from_dict(_item) for _item in obj.get("links")] if obj.get("links") is not None else None
        })
        return _obj
