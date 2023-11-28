# coding: utf-8

"""
    search-api

    These APIs helps to search and suggest based on keyword among available jobs  # noqa: E501

    
"""

from __future__ import absolute_import

import re  # noqa: F401

# python 2 and python 3 compatibility library
import six

from phenom.commons.api_client import ApiClient


class JobsApi(object):

    base_path = "/jobs-api/v1/jobs/search"

    def __init__(self, token, gateway_url, apikey, api_client=None):
        if api_client is None:
            api_client = ApiClient(gateway_url + self.base_path, apikey, token)
        self.api_client = api_client

    def search(self, body, **kwargs):  # noqa: E501
        """Jobs Search  # noqa: E501

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.search(body, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param RefineSearchRequest body: (required)
        :return: RefineSearchResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.search_with_http_info(body, **kwargs)  # noqa: E501
        else:
            (data) = self.search_with_http_info(body, **kwargs)  # noqa: E501
            return data

    def search_with_http_info(self, body, **kwargs):  # noqa: E501
        """Jobs Search  # noqa: E501

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.search_with_http_info(body, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param RefineSearchRequest body: (required)
        :return: RefineSearchResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['body']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in six.iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method search" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'body' is set
        if ('body' not in params or
                params['body'] is None):
            raise ValueError("Missing the required parameter `body` when calling `search`")  # noqa: E501

        collection_formats = {}

        path_params = {}

        query_params = []

        header_params = {}

        form_params = []
        local_var_files = {}

        body_params = None
        if 'body' in params:
            body_params = params['body']
        # HTTP header `Accept`
        header_params['Accept'] = self.api_client.select_header_accept(
            ['application/json'])  # noqa: E501

        # HTTP header `Content-Type`
        header_params['Content-Type'] = self.api_client.select_header_content_type(  # noqa: E501
            ['application/json'])  # noqa: E501

        # Authentication setting
        auth_settings = []  # noqa: E501

        return self.api_client.call_api(
            '/', 'POST',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='RefineSearchResponse',  # noqa: E501
            auth_settings=auth_settings,
            async_req=params.get('async_req'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            collection_formats=collection_formats)

    def suggest(self, search_by, prefix, **kwargs):  # noqa: E501
        """Suggests jobs  # noqa: E501

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.suggest(search_by, prefix, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str search_by: (required)
        :param str prefix: (required)
        :param str limit:
        :return: JobTitlesResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.suggest_with_http_info(search_by, prefix, **kwargs)  # noqa: E501
        else:
            (data) = self.suggest_with_http_info(search_by, prefix, **kwargs)  # noqa: E501
            return data

    def suggest_with_http_info(self, search_by, prefix, **kwargs):  # noqa: E501
        """Suggests jobs  # noqa: E501

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.suggest_with_http_info(search_by, prefix, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str search_by: (required)
        :param str prefix: (required)
        :param str limit:
        :return: JobTitlesResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['search_by', 'prefix', 'limit']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in six.iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method suggest" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'search_by' is set
        if ('search_by' not in params or
                params['search_by'] is None):
            raise ValueError("Missing the required parameter `search_by` when calling `suggest`")  # noqa: E501
        # verify the required parameter 'prefix' is set
        if ('prefix' not in params or
                params['prefix'] is None):
            raise ValueError("Missing the required parameter `prefix` when calling `suggest`")  # noqa: E501

        collection_formats = {}

        path_params = {}

        query_params = []
        if 'search_by' in params:
            query_params.append(('searchBy', params['search_by']))  # noqa: E501
        if 'limit' in params:
            query_params.append(('limit', params['limit']))  # noqa: E501
        if 'prefix' in params:
            query_params.append(('prefix', params['prefix']))  # noqa: E501

        header_params = {}

        form_params = []
        local_var_files = {}

        body_params = None
        # HTTP header `Accept`
        header_params['Accept'] = self.api_client.select_header_accept(
            ['application/json'])  # noqa: E501

        # Authentication setting
        auth_settings = []  # noqa: E501

        return self.api_client.call_api(
            '/suggestions', 'GET',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='JobTitlesResponse',  # noqa: E501
            auth_settings=auth_settings,
            async_req=params.get('async_req'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            collection_formats=collection_formats)
