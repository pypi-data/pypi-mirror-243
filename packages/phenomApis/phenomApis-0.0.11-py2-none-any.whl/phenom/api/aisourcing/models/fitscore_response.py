# coding: utf-8

"""
    aisourcing-api

    AI Matching apis   # noqa: E501

    
"""

import pprint
import re  # noqa: F401

import six

class FitscoreResponse(object):
    """
    Attributes:
      swagger_types (dict): The key is attribute name
                            and the value is attribute type.
      attribute_map (dict): The key is attribute name
                            and the value is json key in definition.
    """
    swagger_types = {
        'status': 'int',
        'result': 'list[FitscoreResponseResult]'
    }

    attribute_map = {
        'status': 'status',
        'result': 'result'
    }

    def __init__(self, status=None, result=None):  # noqa: E501
        """FitscoreResponse - a model defined in Swagger"""  # noqa: E501
        self._status = None
        self._result = None
        self.discriminator = None
        if status is not None:
            self.status = status
        if result is not None:
            self.result = result

    @property
    def status(self):
        """Gets the status of this FitscoreResponse.  # noqa: E501


        :return: The status of this FitscoreResponse.  # noqa: E501
        :rtype: int
        """
        return self._status

    @status.setter
    def status(self, status):
        """Sets the status of this FitscoreResponse.


        :param status: The status of this FitscoreResponse.  # noqa: E501
        :type: int
        """

        self._status = status

    @property
    def result(self):
        """Gets the result of this FitscoreResponse.  # noqa: E501


        :return: The result of this FitscoreResponse.  # noqa: E501
        :rtype: list[FitscoreResponseResult]
        """
        return self._result

    @result.setter
    def result(self, result):
        """Sets the result of this FitscoreResponse.


        :param result: The result of this FitscoreResponse.  # noqa: E501
        :type: list[FitscoreResponseResult]
        """

        self._result = result

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
        if issubclass(FitscoreResponse, dict):
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
        if not isinstance(other, FitscoreResponse):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
