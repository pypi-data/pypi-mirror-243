# coding: utf-8

"""
    FINBOURNE Luminesce Web API

    FINBOURNE Technology  # noqa: E501

    The version of the OpenAPI document: 1.14.38
    Contact: info@finbourne.com
    Generated by: https://openapi-generator.tech
"""


from __future__ import absolute_import

import re  # noqa: F401

# python 2 and python 3 compatibility library
import six

from luminesce.api_client import ApiClient
from luminesce.exceptions import (  # noqa: F401
    ApiTypeError,
    ApiValueError
)


class CurrentTableFieldCatalogApi(object):
    """NOTE: This class is auto generated by OpenAPI Generator
    Ref: https://openapi-generator.tech

    Do not edit the class manually.
    """

    def __init__(self, api_client=None):
        if api_client is None:
            api_client = ApiClient()
        self.api_client = api_client

    def get_catalog(self, **kwargs):  # noqa: E501
        """GetCatalog: Shows Table and Field level information on Providers that are currently running that you have access to (in Json format)  # noqa: E501

         The following LuminesceSql is executed to return this information:  ```sql @reg = select     Name,     min(Description) as Description,     min(DocumentationLink) as DocumentationLink,     iif(Category = 'View' and Client is not null, true, false) as IsView from     Sys.Registration where     Type in ('DirectProvider', 'DataProvider')     and      ShowAll = false group by     1     ;  @fld = select     TableName,     FieldName,     DataType,     FieldType,     IsPrimaryKey,     IsMain,     Description,     ParamDefaultValue,     TableParamColumns from     Sys.Field     ;  @x = select     coalesce(f.TableName, r.Name) as TableName,     coalesce(f.FieldName, 'N/A') as FieldName,     f.DataType,     f.FieldType,     f.IsPrimaryKey,     f.IsMain,     case          when f.TableName is not null then             f.Description         else             r.Name || ' returns a different set of columns depending on use.'         end as Description,     f.ParamDefaultValue,     f.TableParamColumns,     r.Description as ProviderDescription,     r.DocumentationLink,     r.IsView from     @reg r     left outer join @fld f         on r.Name = f.TableName order by     1, 5 desc, 6 desc, 2     ;     ```  The following error codes are to be anticipated with standard Problem Detail reports: - 401 Unauthorized   # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True

        >>> thread = api.get_catalog(async_req=True)
        >>> result = thread.get()

        :param free_text_search: Limit the catalog to only things in some way dealing with the passed in text string
        :type free_text_search: str
        :param json_proper: Should this be text/json (not json-encoded-as-a-string)
        :type json_proper: bool
        :param async_req: Whether to execute the request asynchronously.
        :type async_req: bool, optional
        :param _preload_content: if False, the urllib3.HTTPResponse object will
                                 be returned without reading/decoding response
                                 data. Default is True.
        :type _preload_content: bool, optional
        :param _request_timeout: timeout setting for this request. If one
                                 number provided, it will be total request
                                 timeout. It can also be a pair (tuple) of
                                 (connection, read) timeouts.
        :return: Returns the result object.
                 If the method is called asynchronously,
                 returns the request thread.
        :rtype: str
        """
        kwargs['_return_http_data_only'] = True
        return self.get_catalog_with_http_info(**kwargs)  # noqa: E501

    def get_catalog_with_http_info(self, **kwargs):  # noqa: E501
        """GetCatalog: Shows Table and Field level information on Providers that are currently running that you have access to (in Json format)  # noqa: E501

         The following LuminesceSql is executed to return this information:  ```sql @reg = select     Name,     min(Description) as Description,     min(DocumentationLink) as DocumentationLink,     iif(Category = 'View' and Client is not null, true, false) as IsView from     Sys.Registration where     Type in ('DirectProvider', 'DataProvider')     and      ShowAll = false group by     1     ;  @fld = select     TableName,     FieldName,     DataType,     FieldType,     IsPrimaryKey,     IsMain,     Description,     ParamDefaultValue,     TableParamColumns from     Sys.Field     ;  @x = select     coalesce(f.TableName, r.Name) as TableName,     coalesce(f.FieldName, 'N/A') as FieldName,     f.DataType,     f.FieldType,     f.IsPrimaryKey,     f.IsMain,     case          when f.TableName is not null then             f.Description         else             r.Name || ' returns a different set of columns depending on use.'         end as Description,     f.ParamDefaultValue,     f.TableParamColumns,     r.Description as ProviderDescription,     r.DocumentationLink,     r.IsView from     @reg r     left outer join @fld f         on r.Name = f.TableName order by     1, 5 desc, 6 desc, 2     ;     ```  The following error codes are to be anticipated with standard Problem Detail reports: - 401 Unauthorized   # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True

        >>> thread = api.get_catalog_with_http_info(async_req=True)
        >>> result = thread.get()

        :param free_text_search: Limit the catalog to only things in some way dealing with the passed in text string
        :type free_text_search: str
        :param json_proper: Should this be text/json (not json-encoded-as-a-string)
        :type json_proper: bool
        :param async_req: Whether to execute the request asynchronously.
        :type async_req: bool, optional
        :param _return_http_data_only: response data without head status code
                                       and headers
        :type _return_http_data_only: bool, optional
        :param _preload_content: if False, the urllib3.HTTPResponse object will
                                 be returned without reading/decoding response
                                 data. Default is True.
        :type _preload_content: bool, optional
        :param _request_timeout: timeout setting for this request. If one
                                 number provided, it will be total request
                                 timeout. It can also be a pair (tuple) of
                                 (connection, read) timeouts.
        :param _request_auth: set to override the auth_settings for an a single
                              request; this effectively ignores the authentication
                              in the spec for a single request.
        :type _request_auth: dict, optional
        :return: Returns the result object, the HTTP status code, and the headers.
                 If the method is called asynchronously,
                 returns the request thread.
        :rtype: (str, int, HTTPHeaderDict)
        """

        local_var_params = locals()

        all_params = [
            'free_text_search',
            'json_proper'
        ]
        all_params.extend(
            [
                'async_req',
                '_return_http_data_only',
                '_preload_content',
                '_request_timeout',
                '_request_auth',
                '_headers'
            ]
        )

        for key, val in six.iteritems(local_var_params['kwargs']):
            if key not in all_params:
                raise ApiTypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method get_catalog" % key
                )
            local_var_params[key] = val
        del local_var_params['kwargs']

        collection_formats = {}

        path_params = {}

        query_params = []
        if 'free_text_search' in local_var_params and local_var_params['free_text_search'] is not None:  # noqa: E501
            query_params.append(('freeTextSearch', local_var_params['free_text_search']))  # noqa: E501
        if 'json_proper' in local_var_params and local_var_params['json_proper'] is not None:  # noqa: E501
            query_params.append(('jsonProper', local_var_params['json_proper']))  # noqa: E501

        header_params = dict(local_var_params.get('_headers', {}))

        form_params = []
        local_var_files = {}

        body_params = None
        # HTTP header `Accept`
        header_params['Accept'] = self.api_client.select_header_accept(
            ['text/plain', 'application/json', 'text/json'])  # noqa: E501

        header_params['Accept-Encoding'] = "gzip, deflate, br"


        # set the LUSID header
        header_params['X-LUSID-SDK-Language'] = 'Python'
        header_params['X-LUSID-SDK-Version'] = '1.14.38'

        # Authentication setting
        auth_settings = ['oauth2']  # noqa: E501

        response_types_map = {
            200: "str",
        }

        return self.api_client.call_api(
            '/api/Catalog', 'GET',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_types_map=response_types_map,
            auth_settings=auth_settings,
            async_req=local_var_params.get('async_req'),
            _return_http_data_only=local_var_params.get('_return_http_data_only'),  # noqa: E501
            _preload_content=local_var_params.get('_preload_content', True),
            _request_timeout=local_var_params.get('_request_timeout'),
            collection_formats=collection_formats,
            _request_auth=local_var_params.get('_request_auth'))
