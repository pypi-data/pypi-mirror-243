# coding: utf-8

"""
    ex-search-api

    These APIs helps to search and suggest based on keyword among employee profiles  # noqa: E501

    
"""

import pprint
import re  # noqa: F401

import six

class ErrorResponse(object):
    """
    Attributes:
      swagger_types (dict): The key is attribute name
                            and the value is attribute type.
      attribute_map (dict): The key is attribute name
                            and the value is json key in definition.
    """
    swagger_types = {
        'status': 'int',
        'hits': 'int',
        'total_hits': 'int',
        'data': 'object'
    }

    attribute_map = {
        'status': 'status',
        'hits': 'hits',
        'total_hits': 'totalHits',
        'data': 'data'
    }

    def __init__(self, status=None, hits=None, total_hits=None, data=None):  # noqa: E501
        """ErrorResponse - a model defined in Swagger"""  # noqa: E501
        self._status = None
        self._hits = None
        self._total_hits = None
        self._data = None
        self.discriminator = None
        if status is not None:
            self.status = status
        if hits is not None:
            self.hits = hits
        if total_hits is not None:
            self.total_hits = total_hits
        if data is not None:
            self.data = data

    @property
    def status(self):
        """Gets the status of this ErrorResponse.  # noqa: E501


        :return: The status of this ErrorResponse.  # noqa: E501
        :rtype: int
        """
        return self._status

    @status.setter
    def status(self, status):
        """Sets the status of this ErrorResponse.


        :param status: The status of this ErrorResponse.  # noqa: E501
        :type: int
        """

        self._status = status

    @property
    def hits(self):
        """Gets the hits of this ErrorResponse.  # noqa: E501


        :return: The hits of this ErrorResponse.  # noqa: E501
        :rtype: int
        """
        return self._hits

    @hits.setter
    def hits(self, hits):
        """Sets the hits of this ErrorResponse.


        :param hits: The hits of this ErrorResponse.  # noqa: E501
        :type: int
        """

        self._hits = hits

    @property
    def total_hits(self):
        """Gets the total_hits of this ErrorResponse.  # noqa: E501


        :return: The total_hits of this ErrorResponse.  # noqa: E501
        :rtype: int
        """
        return self._total_hits

    @total_hits.setter
    def total_hits(self, total_hits):
        """Sets the total_hits of this ErrorResponse.


        :param total_hits: The total_hits of this ErrorResponse.  # noqa: E501
        :type: int
        """

        self._total_hits = total_hits

    @property
    def data(self):
        """Gets the data of this ErrorResponse.  # noqa: E501


        :return: The data of this ErrorResponse.  # noqa: E501
        :rtype: object
        """
        return self._data

    @data.setter
    def data(self, data):
        """Sets the data of this ErrorResponse.


        :param data: The data of this ErrorResponse.  # noqa: E501
        :type: object
        """

        self._data = data

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
        if issubclass(ErrorResponse, dict):
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
        if not isinstance(other, ErrorResponse):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
