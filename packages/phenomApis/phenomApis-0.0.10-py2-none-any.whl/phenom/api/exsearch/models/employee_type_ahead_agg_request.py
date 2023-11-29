# coding: utf-8

"""
    ex-search-api

    These APIs helps to search and suggest based on keyword among employee profiles  # noqa: E501

    
"""

import pprint
import re  # noqa: F401

import six

class EmployeeTypeAheadAggRequest(object):
    """
    Attributes:
      swagger_types (dict): The key is attribute name
                            and the value is attribute type.
      attribute_map (dict): The key is attribute name
                            and the value is json key in definition.
    """
    swagger_types = {
        'keyword': 'str',
        'common': 'list[CommonNode]',
        'aggregations': 'list[AggregationsNode]'
    }

    attribute_map = {
        'keyword': 'keyword',
        'common': 'common',
        'aggregations': 'aggregations'
    }

    def __init__(self, keyword=None, common=None, aggregations=None):  # noqa: E501
        """EmployeeTypeAheadAggRequest - a model defined in Swagger"""  # noqa: E501
        self._keyword = None
        self._common = None
        self._aggregations = None
        self.discriminator = None
        if keyword is not None:
            self.keyword = keyword
        if common is not None:
            self.common = common
        if aggregations is not None:
            self.aggregations = aggregations

    @property
    def keyword(self):
        """Gets the keyword of this EmployeeTypeAheadAggRequest.  # noqa: E501

        keyword to search  # noqa: E501

        :return: The keyword of this EmployeeTypeAheadAggRequest.  # noqa: E501
        :rtype: str
        """
        return self._keyword

    @keyword.setter
    def keyword(self, keyword):
        """Sets the keyword of this EmployeeTypeAheadAggRequest.

        keyword to search  # noqa: E501

        :param keyword: The keyword of this EmployeeTypeAheadAggRequest.  # noqa: E501
        :type: str
        """

        self._keyword = keyword

    @property
    def common(self):
        """Gets the common of this EmployeeTypeAheadAggRequest.  # noqa: E501


        :return: The common of this EmployeeTypeAheadAggRequest.  # noqa: E501
        :rtype: list[CommonNode]
        """
        return self._common

    @common.setter
    def common(self, common):
        """Sets the common of this EmployeeTypeAheadAggRequest.


        :param common: The common of this EmployeeTypeAheadAggRequest.  # noqa: E501
        :type: list[CommonNode]
        """

        self._common = common

    @property
    def aggregations(self):
        """Gets the aggregations of this EmployeeTypeAheadAggRequest.  # noqa: E501


        :return: The aggregations of this EmployeeTypeAheadAggRequest.  # noqa: E501
        :rtype: list[AggregationsNode]
        """
        return self._aggregations

    @aggregations.setter
    def aggregations(self, aggregations):
        """Sets the aggregations of this EmployeeTypeAheadAggRequest.


        :param aggregations: The aggregations of this EmployeeTypeAheadAggRequest.  # noqa: E501
        :type: list[AggregationsNode]
        """

        self._aggregations = aggregations

    def to_dict(self):
        """Returns the model properties as a dict"""
        result = {}

        for attr, _ in six.iteritems(self.swagger_types):
            value = getattr(self, attr)
            if isinstance(value, list):
                result[attr] = list(map(
                    lambda x: x.to_dict() if hasattr(x, "to_dict") else x,
                    value
                ))
            elif hasattr(value, "to_dict"):
                result[attr] = value.to_dict()
            elif isinstance(value, dict):
                result[attr] = dict(map(
                    lambda item: (item[0], item[1].to_dict())
                    if hasattr(item[1], "to_dict") else item,
                    value.items()
                ))
            else:
                result[attr] = value
        if issubclass(EmployeeTypeAheadAggRequest, dict):
            for key, value in self.items():
                result[key] = value

        return result

    def to_str(self):
        """Returns the string representation of the model"""
        return pprint.pformat(self.to_dict())

    def __repr__(self):
        """For `print` and `pprint`"""
        return self.to_str()

    def __eq__(self, other):
        """Returns true if both objects are equal"""
        if not isinstance(other, EmployeeTypeAheadAggRequest):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
