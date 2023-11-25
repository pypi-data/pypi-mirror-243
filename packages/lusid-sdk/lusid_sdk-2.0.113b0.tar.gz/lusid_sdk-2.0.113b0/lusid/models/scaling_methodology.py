# coding: utf-8

"""
    LUSID API

    FINBOURNE Technology  # noqa: E501

    Contact: info@finbourne.com
    Generated by OpenAPI Generator (https://openapi-generator.tech)

    Do not edit the class manually.
"""


import json
import pprint
import re  # noqa: F401
from aenum import Enum, no_arg





class ScalingMethodology(str, Enum):
    """
    ScalingMethodology
    """

    """
    allowed enum values
    """
    SUM = 'Sum'
    ABSOLUTESUM = 'AbsoluteSum'
    UNITY = 'Unity'

    @classmethod
    def from_json(cls, json_str: str) -> ScalingMethodology:
        """Create an instance of ScalingMethodology from a JSON string"""
        return ScalingMethodology(json.loads(json_str))
