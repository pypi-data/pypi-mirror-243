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





class MarketDataType(str, Enum):
    """
    The format of the complex market data stored. Complex market data is used to store any  data which requires more context than just a simple single point as is the case with a  quote.  Examples of such complex market data are Discount Curve and Volatility Surfaces.
    """

    """
    allowed enum values
    """
    DISCOUNTFACTORCURVEDATA = 'DiscountFactorCurveData'
    EQUITYVOLSURFACEDATA = 'EquityVolSurfaceData'
    FXVOLSURFACEDATA = 'FxVolSurfaceData'
    IRVOLCUBEDATA = 'IrVolCubeData'
    OPAQUEMARKETDATA = 'OpaqueMarketData'
    YIELDCURVEDATA = 'YieldCurveData'
    FXFORWARDCURVEDATA = 'FxForwardCurveData'
    FXFORWARDPIPSCURVEDATA = 'FxForwardPipsCurveData'
    FXFORWARDTENORCURVEDATA = 'FxForwardTenorCurveData'
    FXFORWARDTENORPIPSCURVEDATA = 'FxForwardTenorPipsCurveData'
    FXFORWARDCURVEBYQUOTEREFERENCE = 'FxForwardCurveByQuoteReference'
    CREDITSPREADCURVEDATA = 'CreditSpreadCurveData'
    EQUITYCURVEBYPRICESDATA = 'EquityCurveByPricesData'

    @classmethod
    def from_json(cls, json_str: str) -> MarketDataType:
        """Create an instance of MarketDataType from a JSON string"""
        return MarketDataType(json.loads(json_str))
