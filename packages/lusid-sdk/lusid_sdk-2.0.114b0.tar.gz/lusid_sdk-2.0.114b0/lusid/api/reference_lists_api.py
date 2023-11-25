# coding: utf-8

"""
    LUSID API

    FINBOURNE Technology  # noqa: E501

    Contact: info@finbourne.com
    Generated by OpenAPI Generator (https://openapi-generator.tech)

    Do not edit the class manually.
"""


import re  # noqa: F401
import io
import warnings

from pydantic import validate_arguments, ValidationError
from typing import overload, Optional, Union, Awaitable

from typing_extensions import Annotated
from datetime import datetime

from pydantic import Field, conint, constr, validator

from typing import Optional

from lusid.models.deleted_entity_response import DeletedEntityResponse
from lusid.models.paged_resource_list_of_reference_list_response import PagedResourceListOfReferenceListResponse
from lusid.models.reference_list_request import ReferenceListRequest
from lusid.models.reference_list_response import ReferenceListResponse

from lusid.api_client import ApiClient
from lusid.api_response import ApiResponse
from lusid.exceptions import (  # noqa: F401
    ApiTypeError,
    ApiValueError
)


class ReferenceListsApi:
    """NOTE: This class is auto generated by OpenAPI Generator
    Ref: https://openapi-generator.tech

    Do not edit the class manually.
    """

    def __init__(self, api_client=None) -> None:
        if api_client is None:
            api_client = ApiClient.get_default()
        self.api_client = api_client

    @overload
    async def delete_reference_list(self, scope : Annotated[constr(strict=True, max_length=64, min_length=1), Field(..., description="The scope to which the Reference List belongs.")], code : Annotated[constr(strict=True, max_length=64, min_length=1), Field(..., description="The Reference List's unique identifier.")], **kwargs) -> DeletedEntityResponse:  # noqa: E501
        ...

    @overload
    def delete_reference_list(self, scope : Annotated[constr(strict=True, max_length=64, min_length=1), Field(..., description="The scope to which the Reference List belongs.")], code : Annotated[constr(strict=True, max_length=64, min_length=1), Field(..., description="The Reference List's unique identifier.")], async_req: Optional[bool]=True, **kwargs) -> DeletedEntityResponse:  # noqa: E501
        ...

    @validate_arguments
    def delete_reference_list(self, scope : Annotated[constr(strict=True, max_length=64, min_length=1), Field(..., description="The scope to which the Reference List belongs.")], code : Annotated[constr(strict=True, max_length=64, min_length=1), Field(..., description="The Reference List's unique identifier.")], async_req: Optional[bool]=None, **kwargs) -> Union[DeletedEntityResponse, Awaitable[DeletedEntityResponse]]:  # noqa: E501
        """[EARLY ACCESS] DeleteReferenceList: Delete Reference List  # noqa: E501

        Delete a Reference List instance.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True

        >>> thread = api.delete_reference_list(scope, code, async_req=True)
        >>> result = thread.get()

        :param scope: The scope to which the Reference List belongs. (required)
        :type scope: str
        :param code: The Reference List's unique identifier. (required)
        :type code: str
        :param async_req: Whether to execute the request asynchronously.
        :type async_req: bool, optional
        :param _request_timeout: timeout setting for this request.
               If one number provided, it will be total request
               timeout. It can also be a pair (tuple) of
               (connection, read) timeouts.
        :return: Returns the result object.
                 If the method is called asynchronously,
                 returns the request thread.
        :rtype: DeletedEntityResponse
        """
        kwargs['_return_http_data_only'] = True
        if '_preload_content' in kwargs:
            message = "Error! Please call the delete_reference_list_with_http_info method with `_preload_content` instead and obtain raw data from ApiResponse.raw_data"  # noqa: E501
            raise ValueError(message)
        if async_req is not None:
            kwargs['async_req'] = async_req
        return self.delete_reference_list_with_http_info(scope, code, **kwargs)  # noqa: E501

    @validate_arguments
    def delete_reference_list_with_http_info(self, scope : Annotated[constr(strict=True, max_length=64, min_length=1), Field(..., description="The scope to which the Reference List belongs.")], code : Annotated[constr(strict=True, max_length=64, min_length=1), Field(..., description="The Reference List's unique identifier.")], **kwargs) -> ApiResponse:  # noqa: E501
        """[EARLY ACCESS] DeleteReferenceList: Delete Reference List  # noqa: E501

        Delete a Reference List instance.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True

        >>> thread = api.delete_reference_list_with_http_info(scope, code, async_req=True)
        >>> result = thread.get()

        :param scope: The scope to which the Reference List belongs. (required)
        :type scope: str
        :param code: The Reference List's unique identifier. (required)
        :type code: str
        :param async_req: Whether to execute the request asynchronously.
        :type async_req: bool, optional
        :param _preload_content: if False, the ApiResponse.data will
                                 be set to none and raw_data will store the
                                 HTTP response body without reading/decoding.
                                 Default is True.
        :type _preload_content: bool, optional
        :param _return_http_data_only: response data instead of ApiResponse
                                       object with status code, headers, etc
        :type _return_http_data_only: bool, optional
        :param _request_timeout: timeout setting for this request. If one
                                 number provided, it will be total request
                                 timeout. It can also be a pair (tuple) of
                                 (connection, read) timeouts.
        :param _request_auth: set to override the auth_settings for an a single
                              request; this effectively ignores the authentication
                              in the spec for a single request.
        :type _request_auth: dict, optional
        :type _content_type: string, optional: force content-type for the request
        :return: Returns the result object.
                 If the method is called asynchronously,
                 returns the request thread.
        :rtype: tuple(DeletedEntityResponse, status_code(int), headers(HTTPHeaderDict))
        """

        _params = locals()

        _all_params = [
            'scope',
            'code'
        ]
        _all_params.extend(
            [
                'async_req',
                '_return_http_data_only',
                '_preload_content',
                '_request_timeout',
                '_request_auth',
                '_content_type',
                '_headers'
            ]
        )

        # validate the arguments
        for _key, _val in _params['kwargs'].items():
            if _key not in _all_params:
                raise ApiTypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method delete_reference_list" % _key
                )
            _params[_key] = _val
        del _params['kwargs']

        _collection_formats = {}

        # process the path parameters
        _path_params = {}
        if _params['scope']:
            _path_params['scope'] = _params['scope']

        if _params['code']:
            _path_params['code'] = _params['code']


        # process the query parameters
        _query_params = []
        # process the header parameters
        _header_params = dict(_params.get('_headers', {}))
        # process the form parameters
        _form_params = []
        _files = {}
        # process the body parameter
        _body_params = None
        # set the HTTP header `Accept`
        _header_params['Accept'] = self.api_client.select_header_accept(
            ['text/plain', 'application/json', 'text/json'])  # noqa: E501

        # authentication setting
        _auth_settings = ['oauth2']  # noqa: E501

        _response_types_map = {
            '200': "DeletedEntityResponse",
            '400': "LusidValidationProblemDetails",
        }

        return self.api_client.call_api(
            '/api/referencelists/{scope}/{code}', 'DELETE',
            _path_params,
            _query_params,
            _header_params,
            body=_body_params,
            post_params=_form_params,
            files=_files,
            response_types_map=_response_types_map,
            auth_settings=_auth_settings,
            async_req=_params.get('async_req'),
            _return_http_data_only=_params.get('_return_http_data_only'),  # noqa: E501
            _preload_content=_params.get('_preload_content', True),
            _request_timeout=_params.get('_request_timeout'),
            collection_formats=_collection_formats,
            _request_auth=_params.get('_request_auth'))

    @overload
    async def get_reference_list(self, scope : Annotated[constr(strict=True, max_length=64, min_length=1), Field(..., description="The scope to which the Reference List belongs.")], code : Annotated[constr(strict=True, max_length=64, min_length=1), Field(..., description="The Reference List's unique identifier.")], as_at : Annotated[Optional[datetime], Field(description="The asAt datetime at which to retrieve the Reference List. Defaults to return the latest version of the Reference List if not specified.")] = None, **kwargs) -> ReferenceListResponse:  # noqa: E501
        ...

    @overload
    def get_reference_list(self, scope : Annotated[constr(strict=True, max_length=64, min_length=1), Field(..., description="The scope to which the Reference List belongs.")], code : Annotated[constr(strict=True, max_length=64, min_length=1), Field(..., description="The Reference List's unique identifier.")], as_at : Annotated[Optional[datetime], Field(description="The asAt datetime at which to retrieve the Reference List. Defaults to return the latest version of the Reference List if not specified.")] = None, async_req: Optional[bool]=True, **kwargs) -> ReferenceListResponse:  # noqa: E501
        ...

    @validate_arguments
    def get_reference_list(self, scope : Annotated[constr(strict=True, max_length=64, min_length=1), Field(..., description="The scope to which the Reference List belongs.")], code : Annotated[constr(strict=True, max_length=64, min_length=1), Field(..., description="The Reference List's unique identifier.")], as_at : Annotated[Optional[datetime], Field(description="The asAt datetime at which to retrieve the Reference List. Defaults to return the latest version of the Reference List if not specified.")] = None, async_req: Optional[bool]=None, **kwargs) -> Union[ReferenceListResponse, Awaitable[ReferenceListResponse]]:  # noqa: E501
        """[EARLY ACCESS] GetReferenceList: Get Reference List  # noqa: E501

        Retrieve a Reference List instance at a point in AsAt time.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True

        >>> thread = api.get_reference_list(scope, code, as_at, async_req=True)
        >>> result = thread.get()

        :param scope: The scope to which the Reference List belongs. (required)
        :type scope: str
        :param code: The Reference List's unique identifier. (required)
        :type code: str
        :param as_at: The asAt datetime at which to retrieve the Reference List. Defaults to return the latest version of the Reference List if not specified.
        :type as_at: datetime
        :param async_req: Whether to execute the request asynchronously.
        :type async_req: bool, optional
        :param _request_timeout: timeout setting for this request.
               If one number provided, it will be total request
               timeout. It can also be a pair (tuple) of
               (connection, read) timeouts.
        :return: Returns the result object.
                 If the method is called asynchronously,
                 returns the request thread.
        :rtype: ReferenceListResponse
        """
        kwargs['_return_http_data_only'] = True
        if '_preload_content' in kwargs:
            message = "Error! Please call the get_reference_list_with_http_info method with `_preload_content` instead and obtain raw data from ApiResponse.raw_data"  # noqa: E501
            raise ValueError(message)
        if async_req is not None:
            kwargs['async_req'] = async_req
        return self.get_reference_list_with_http_info(scope, code, as_at, **kwargs)  # noqa: E501

    @validate_arguments
    def get_reference_list_with_http_info(self, scope : Annotated[constr(strict=True, max_length=64, min_length=1), Field(..., description="The scope to which the Reference List belongs.")], code : Annotated[constr(strict=True, max_length=64, min_length=1), Field(..., description="The Reference List's unique identifier.")], as_at : Annotated[Optional[datetime], Field(description="The asAt datetime at which to retrieve the Reference List. Defaults to return the latest version of the Reference List if not specified.")] = None, **kwargs) -> ApiResponse:  # noqa: E501
        """[EARLY ACCESS] GetReferenceList: Get Reference List  # noqa: E501

        Retrieve a Reference List instance at a point in AsAt time.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True

        >>> thread = api.get_reference_list_with_http_info(scope, code, as_at, async_req=True)
        >>> result = thread.get()

        :param scope: The scope to which the Reference List belongs. (required)
        :type scope: str
        :param code: The Reference List's unique identifier. (required)
        :type code: str
        :param as_at: The asAt datetime at which to retrieve the Reference List. Defaults to return the latest version of the Reference List if not specified.
        :type as_at: datetime
        :param async_req: Whether to execute the request asynchronously.
        :type async_req: bool, optional
        :param _preload_content: if False, the ApiResponse.data will
                                 be set to none and raw_data will store the
                                 HTTP response body without reading/decoding.
                                 Default is True.
        :type _preload_content: bool, optional
        :param _return_http_data_only: response data instead of ApiResponse
                                       object with status code, headers, etc
        :type _return_http_data_only: bool, optional
        :param _request_timeout: timeout setting for this request. If one
                                 number provided, it will be total request
                                 timeout. It can also be a pair (tuple) of
                                 (connection, read) timeouts.
        :param _request_auth: set to override the auth_settings for an a single
                              request; this effectively ignores the authentication
                              in the spec for a single request.
        :type _request_auth: dict, optional
        :type _content_type: string, optional: force content-type for the request
        :return: Returns the result object.
                 If the method is called asynchronously,
                 returns the request thread.
        :rtype: tuple(ReferenceListResponse, status_code(int), headers(HTTPHeaderDict))
        """

        _params = locals()

        _all_params = [
            'scope',
            'code',
            'as_at'
        ]
        _all_params.extend(
            [
                'async_req',
                '_return_http_data_only',
                '_preload_content',
                '_request_timeout',
                '_request_auth',
                '_content_type',
                '_headers'
            ]
        )

        # validate the arguments
        for _key, _val in _params['kwargs'].items():
            if _key not in _all_params:
                raise ApiTypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method get_reference_list" % _key
                )
            _params[_key] = _val
        del _params['kwargs']

        _collection_formats = {}

        # process the path parameters
        _path_params = {}
        if _params['scope']:
            _path_params['scope'] = _params['scope']

        if _params['code']:
            _path_params['code'] = _params['code']


        # process the query parameters
        _query_params = []
        if _params.get('as_at') is not None:  # noqa: E501
            if isinstance(_params['as_at'], datetime):
                _query_params.append(('asAt', _params['as_at'].strftime(self.api_client.configuration.datetime_format)))
            else:
                _query_params.append(('asAt', _params['as_at']))

        # process the header parameters
        _header_params = dict(_params.get('_headers', {}))
        # process the form parameters
        _form_params = []
        _files = {}
        # process the body parameter
        _body_params = None
        # set the HTTP header `Accept`
        _header_params['Accept'] = self.api_client.select_header_accept(
            ['text/plain', 'application/json', 'text/json'])  # noqa: E501

        # authentication setting
        _auth_settings = ['oauth2']  # noqa: E501

        _response_types_map = {
            '200': "ReferenceListResponse",
            '400': "LusidValidationProblemDetails",
        }

        return self.api_client.call_api(
            '/api/referencelists/{scope}/{code}', 'GET',
            _path_params,
            _query_params,
            _header_params,
            body=_body_params,
            post_params=_form_params,
            files=_files,
            response_types_map=_response_types_map,
            auth_settings=_auth_settings,
            async_req=_params.get('async_req'),
            _return_http_data_only=_params.get('_return_http_data_only'),  # noqa: E501
            _preload_content=_params.get('_preload_content', True),
            _request_timeout=_params.get('_request_timeout'),
            collection_formats=_collection_formats,
            _request_auth=_params.get('_request_auth'))

    @overload
    async def list_reference_lists(self, as_at : Annotated[Optional[datetime], Field(description="The asAt datetime at which to list Reference Lists. Defaults to return the latest version of Reference Lists if not specified.")] = None, page : Annotated[Optional[constr(strict=True, max_length=500, min_length=1)], Field(description="The pagination token to use to continue listing Reference Lists from a previous call to list Reference Lists.              This value is returned from the previous call. If a pagination token is provided, the filter, limit and asAt fields              must not have changed since the original request.")] = None, limit : Annotated[Optional[conint(strict=True, le=5000, ge=1)], Field(description="When paginating, limit the number of returned results to this number. Defaults to 100 if not specified.")] = None, filter : Annotated[Optional[constr(strict=True, max_length=16384, min_length=0)], Field(description="Expression to filter the result set. Read more about filtering results from LUSID here:              https://support.lusid.com/filtering-results-from-lusid.")] = None, **kwargs) -> PagedResourceListOfReferenceListResponse:  # noqa: E501
        ...

    @overload
    def list_reference_lists(self, as_at : Annotated[Optional[datetime], Field(description="The asAt datetime at which to list Reference Lists. Defaults to return the latest version of Reference Lists if not specified.")] = None, page : Annotated[Optional[constr(strict=True, max_length=500, min_length=1)], Field(description="The pagination token to use to continue listing Reference Lists from a previous call to list Reference Lists.              This value is returned from the previous call. If a pagination token is provided, the filter, limit and asAt fields              must not have changed since the original request.")] = None, limit : Annotated[Optional[conint(strict=True, le=5000, ge=1)], Field(description="When paginating, limit the number of returned results to this number. Defaults to 100 if not specified.")] = None, filter : Annotated[Optional[constr(strict=True, max_length=16384, min_length=0)], Field(description="Expression to filter the result set. Read more about filtering results from LUSID here:              https://support.lusid.com/filtering-results-from-lusid.")] = None, async_req: Optional[bool]=True, **kwargs) -> PagedResourceListOfReferenceListResponse:  # noqa: E501
        ...

    @validate_arguments
    def list_reference_lists(self, as_at : Annotated[Optional[datetime], Field(description="The asAt datetime at which to list Reference Lists. Defaults to return the latest version of Reference Lists if not specified.")] = None, page : Annotated[Optional[constr(strict=True, max_length=500, min_length=1)], Field(description="The pagination token to use to continue listing Reference Lists from a previous call to list Reference Lists.              This value is returned from the previous call. If a pagination token is provided, the filter, limit and asAt fields              must not have changed since the original request.")] = None, limit : Annotated[Optional[conint(strict=True, le=5000, ge=1)], Field(description="When paginating, limit the number of returned results to this number. Defaults to 100 if not specified.")] = None, filter : Annotated[Optional[constr(strict=True, max_length=16384, min_length=0)], Field(description="Expression to filter the result set. Read more about filtering results from LUSID here:              https://support.lusid.com/filtering-results-from-lusid.")] = None, async_req: Optional[bool]=None, **kwargs) -> Union[PagedResourceListOfReferenceListResponse, Awaitable[PagedResourceListOfReferenceListResponse]]:  # noqa: E501
        """[EARLY ACCESS] ListReferenceLists: List Reference Lists  # noqa: E501

        List all the Reference Lists matching particular criteria.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True

        >>> thread = api.list_reference_lists(as_at, page, limit, filter, async_req=True)
        >>> result = thread.get()

        :param as_at: The asAt datetime at which to list Reference Lists. Defaults to return the latest version of Reference Lists if not specified.
        :type as_at: datetime
        :param page: The pagination token to use to continue listing Reference Lists from a previous call to list Reference Lists.              This value is returned from the previous call. If a pagination token is provided, the filter, limit and asAt fields              must not have changed since the original request.
        :type page: str
        :param limit: When paginating, limit the number of returned results to this number. Defaults to 100 if not specified.
        :type limit: int
        :param filter: Expression to filter the result set. Read more about filtering results from LUSID here:              https://support.lusid.com/filtering-results-from-lusid.
        :type filter: str
        :param async_req: Whether to execute the request asynchronously.
        :type async_req: bool, optional
        :param _request_timeout: timeout setting for this request.
               If one number provided, it will be total request
               timeout. It can also be a pair (tuple) of
               (connection, read) timeouts.
        :return: Returns the result object.
                 If the method is called asynchronously,
                 returns the request thread.
        :rtype: PagedResourceListOfReferenceListResponse
        """
        kwargs['_return_http_data_only'] = True
        if '_preload_content' in kwargs:
            message = "Error! Please call the list_reference_lists_with_http_info method with `_preload_content` instead and obtain raw data from ApiResponse.raw_data"  # noqa: E501
            raise ValueError(message)
        if async_req is not None:
            kwargs['async_req'] = async_req
        return self.list_reference_lists_with_http_info(as_at, page, limit, filter, **kwargs)  # noqa: E501

    @validate_arguments
    def list_reference_lists_with_http_info(self, as_at : Annotated[Optional[datetime], Field(description="The asAt datetime at which to list Reference Lists. Defaults to return the latest version of Reference Lists if not specified.")] = None, page : Annotated[Optional[constr(strict=True, max_length=500, min_length=1)], Field(description="The pagination token to use to continue listing Reference Lists from a previous call to list Reference Lists.              This value is returned from the previous call. If a pagination token is provided, the filter, limit and asAt fields              must not have changed since the original request.")] = None, limit : Annotated[Optional[conint(strict=True, le=5000, ge=1)], Field(description="When paginating, limit the number of returned results to this number. Defaults to 100 if not specified.")] = None, filter : Annotated[Optional[constr(strict=True, max_length=16384, min_length=0)], Field(description="Expression to filter the result set. Read more about filtering results from LUSID here:              https://support.lusid.com/filtering-results-from-lusid.")] = None, **kwargs) -> ApiResponse:  # noqa: E501
        """[EARLY ACCESS] ListReferenceLists: List Reference Lists  # noqa: E501

        List all the Reference Lists matching particular criteria.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True

        >>> thread = api.list_reference_lists_with_http_info(as_at, page, limit, filter, async_req=True)
        >>> result = thread.get()

        :param as_at: The asAt datetime at which to list Reference Lists. Defaults to return the latest version of Reference Lists if not specified.
        :type as_at: datetime
        :param page: The pagination token to use to continue listing Reference Lists from a previous call to list Reference Lists.              This value is returned from the previous call. If a pagination token is provided, the filter, limit and asAt fields              must not have changed since the original request.
        :type page: str
        :param limit: When paginating, limit the number of returned results to this number. Defaults to 100 if not specified.
        :type limit: int
        :param filter: Expression to filter the result set. Read more about filtering results from LUSID here:              https://support.lusid.com/filtering-results-from-lusid.
        :type filter: str
        :param async_req: Whether to execute the request asynchronously.
        :type async_req: bool, optional
        :param _preload_content: if False, the ApiResponse.data will
                                 be set to none and raw_data will store the
                                 HTTP response body without reading/decoding.
                                 Default is True.
        :type _preload_content: bool, optional
        :param _return_http_data_only: response data instead of ApiResponse
                                       object with status code, headers, etc
        :type _return_http_data_only: bool, optional
        :param _request_timeout: timeout setting for this request. If one
                                 number provided, it will be total request
                                 timeout. It can also be a pair (tuple) of
                                 (connection, read) timeouts.
        :param _request_auth: set to override the auth_settings for an a single
                              request; this effectively ignores the authentication
                              in the spec for a single request.
        :type _request_auth: dict, optional
        :type _content_type: string, optional: force content-type for the request
        :return: Returns the result object.
                 If the method is called asynchronously,
                 returns the request thread.
        :rtype: tuple(PagedResourceListOfReferenceListResponse, status_code(int), headers(HTTPHeaderDict))
        """

        _params = locals()

        _all_params = [
            'as_at',
            'page',
            'limit',
            'filter'
        ]
        _all_params.extend(
            [
                'async_req',
                '_return_http_data_only',
                '_preload_content',
                '_request_timeout',
                '_request_auth',
                '_content_type',
                '_headers'
            ]
        )

        # validate the arguments
        for _key, _val in _params['kwargs'].items():
            if _key not in _all_params:
                raise ApiTypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method list_reference_lists" % _key
                )
            _params[_key] = _val
        del _params['kwargs']

        _collection_formats = {}

        # process the path parameters
        _path_params = {}

        # process the query parameters
        _query_params = []
        if _params.get('as_at') is not None:  # noqa: E501
            if isinstance(_params['as_at'], datetime):
                _query_params.append(('asAt', _params['as_at'].strftime(self.api_client.configuration.datetime_format)))
            else:
                _query_params.append(('asAt', _params['as_at']))

        if _params.get('page') is not None:  # noqa: E501
            _query_params.append(('page', _params['page']))

        if _params.get('limit') is not None:  # noqa: E501
            _query_params.append(('limit', _params['limit']))

        if _params.get('filter') is not None:  # noqa: E501
            _query_params.append(('filter', _params['filter']))

        # process the header parameters
        _header_params = dict(_params.get('_headers', {}))
        # process the form parameters
        _form_params = []
        _files = {}
        # process the body parameter
        _body_params = None
        # set the HTTP header `Accept`
        _header_params['Accept'] = self.api_client.select_header_accept(
            ['text/plain', 'application/json', 'text/json'])  # noqa: E501

        # authentication setting
        _auth_settings = ['oauth2']  # noqa: E501

        _response_types_map = {
            '200': "PagedResourceListOfReferenceListResponse",
            '400': "LusidValidationProblemDetails",
        }

        return self.api_client.call_api(
            '/api/referencelists', 'GET',
            _path_params,
            _query_params,
            _header_params,
            body=_body_params,
            post_params=_form_params,
            files=_files,
            response_types_map=_response_types_map,
            auth_settings=_auth_settings,
            async_req=_params.get('async_req'),
            _return_http_data_only=_params.get('_return_http_data_only'),  # noqa: E501
            _preload_content=_params.get('_preload_content', True),
            _request_timeout=_params.get('_request_timeout'),
            collection_formats=_collection_formats,
            _request_auth=_params.get('_request_auth'))

    @overload
    async def upsert_reference_list(self, reference_list_request : Annotated[Optional[ReferenceListRequest], Field(description="The payload describing the Reference List instance.")] = None, **kwargs) -> ReferenceListResponse:  # noqa: E501
        ...

    @overload
    def upsert_reference_list(self, reference_list_request : Annotated[Optional[ReferenceListRequest], Field(description="The payload describing the Reference List instance.")] = None, async_req: Optional[bool]=True, **kwargs) -> ReferenceListResponse:  # noqa: E501
        ...

    @validate_arguments
    def upsert_reference_list(self, reference_list_request : Annotated[Optional[ReferenceListRequest], Field(description="The payload describing the Reference List instance.")] = None, async_req: Optional[bool]=None, **kwargs) -> Union[ReferenceListResponse, Awaitable[ReferenceListResponse]]:  # noqa: E501
        """[EARLY ACCESS] UpsertReferenceList: Upsert Reference List  # noqa: E501

        Insert the Reference List if it does not exist or update the Reference List with the supplied state if it does exist.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True

        >>> thread = api.upsert_reference_list(reference_list_request, async_req=True)
        >>> result = thread.get()

        :param reference_list_request: The payload describing the Reference List instance.
        :type reference_list_request: ReferenceListRequest
        :param async_req: Whether to execute the request asynchronously.
        :type async_req: bool, optional
        :param _request_timeout: timeout setting for this request.
               If one number provided, it will be total request
               timeout. It can also be a pair (tuple) of
               (connection, read) timeouts.
        :return: Returns the result object.
                 If the method is called asynchronously,
                 returns the request thread.
        :rtype: ReferenceListResponse
        """
        kwargs['_return_http_data_only'] = True
        if '_preload_content' in kwargs:
            message = "Error! Please call the upsert_reference_list_with_http_info method with `_preload_content` instead and obtain raw data from ApiResponse.raw_data"  # noqa: E501
            raise ValueError(message)
        if async_req is not None:
            kwargs['async_req'] = async_req
        return self.upsert_reference_list_with_http_info(reference_list_request, **kwargs)  # noqa: E501

    @validate_arguments
    def upsert_reference_list_with_http_info(self, reference_list_request : Annotated[Optional[ReferenceListRequest], Field(description="The payload describing the Reference List instance.")] = None, **kwargs) -> ApiResponse:  # noqa: E501
        """[EARLY ACCESS] UpsertReferenceList: Upsert Reference List  # noqa: E501

        Insert the Reference List if it does not exist or update the Reference List with the supplied state if it does exist.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True

        >>> thread = api.upsert_reference_list_with_http_info(reference_list_request, async_req=True)
        >>> result = thread.get()

        :param reference_list_request: The payload describing the Reference List instance.
        :type reference_list_request: ReferenceListRequest
        :param async_req: Whether to execute the request asynchronously.
        :type async_req: bool, optional
        :param _preload_content: if False, the ApiResponse.data will
                                 be set to none and raw_data will store the
                                 HTTP response body without reading/decoding.
                                 Default is True.
        :type _preload_content: bool, optional
        :param _return_http_data_only: response data instead of ApiResponse
                                       object with status code, headers, etc
        :type _return_http_data_only: bool, optional
        :param _request_timeout: timeout setting for this request. If one
                                 number provided, it will be total request
                                 timeout. It can also be a pair (tuple) of
                                 (connection, read) timeouts.
        :param _request_auth: set to override the auth_settings for an a single
                              request; this effectively ignores the authentication
                              in the spec for a single request.
        :type _request_auth: dict, optional
        :type _content_type: string, optional: force content-type for the request
        :return: Returns the result object.
                 If the method is called asynchronously,
                 returns the request thread.
        :rtype: tuple(ReferenceListResponse, status_code(int), headers(HTTPHeaderDict))
        """

        _params = locals()

        _all_params = [
            'reference_list_request'
        ]
        _all_params.extend(
            [
                'async_req',
                '_return_http_data_only',
                '_preload_content',
                '_request_timeout',
                '_request_auth',
                '_content_type',
                '_headers'
            ]
        )

        # validate the arguments
        for _key, _val in _params['kwargs'].items():
            if _key not in _all_params:
                raise ApiTypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method upsert_reference_list" % _key
                )
            _params[_key] = _val
        del _params['kwargs']

        _collection_formats = {}

        # process the path parameters
        _path_params = {}

        # process the query parameters
        _query_params = []
        # process the header parameters
        _header_params = dict(_params.get('_headers', {}))
        # process the form parameters
        _form_params = []
        _files = {}
        # process the body parameter
        _body_params = None
        if _params['reference_list_request'] is not None:
            _body_params = _params['reference_list_request']

        # set the HTTP header `Accept`
        _header_params['Accept'] = self.api_client.select_header_accept(
            ['text/plain', 'application/json', 'text/json'])  # noqa: E501

        # set the HTTP header `Content-Type`
        _content_types_list = _params.get('_content_type',
            self.api_client.select_header_content_type(
                ['application/json-patch+json', 'application/json', 'text/json', 'application/*+json']))
        if _content_types_list:
                _header_params['Content-Type'] = _content_types_list

        # authentication setting
        _auth_settings = ['oauth2']  # noqa: E501

        _response_types_map = {
            '200': "ReferenceListResponse",
            '400': "LusidValidationProblemDetails",
        }

        return self.api_client.call_api(
            '/api/referencelists', 'POST',
            _path_params,
            _query_params,
            _header_params,
            body=_body_params,
            post_params=_form_params,
            files=_files,
            response_types_map=_response_types_map,
            auth_settings=_auth_settings,
            async_req=_params.get('async_req'),
            _return_http_data_only=_params.get('_return_http_data_only'),  # noqa: E501
            _preload_content=_params.get('_preload_content', True),
            _request_timeout=_params.get('_request_timeout'),
            collection_formats=_collection_formats,
            _request_auth=_params.get('_request_auth'))
