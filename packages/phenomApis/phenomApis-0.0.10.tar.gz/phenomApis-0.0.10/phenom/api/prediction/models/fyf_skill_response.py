# coding: utf-8

"""
    prediction-api

    Prediction api   # noqa: E501

    
"""

import pprint
import re  # noqa: F401

import six

class FYFSkillResponse(object):
    """
    Attributes:
      swagger_types (dict): The key is attribute name
                            and the value is attribute type.
      attribute_map (dict): The key is attribute name
                            and the value is json key in definition.
    """
    swagger_types = {
        'status': 'str',
        'total_hits': 'int',
        'data': 'SkillResults',
        'message': 'str'
    }

    attribute_map = {
        'status': 'status',
        'total_hits': 'totalHits',
        'data': 'data',
        'message': 'message'
    }

    def __init__(self, status=None, total_hits=None, data=None, message=None):  # noqa: E501
        """FYFSkillResponse - a model defined in Swagger"""  # noqa: E501
        self._status = None
        self._total_hits = None
        self._data = None
        self._message = None
        self.discriminator = None
        self.status = status
        if total_hits is not None:
            self.total_hits = total_hits
        if data is not None:
            self.data = data
        if message is not None:
            self.message = message

    @property
    def status(self):
        """Gets the status of this FYFSkillResponse.  # noqa: E501


        :return: The status of this FYFSkillResponse.  # noqa: E501
        :rtype: str
        """
        return self._status

    @status.setter
    def status(self, status):
        """Sets the status of this FYFSkillResponse.


        :param status: The status of this FYFSkillResponse.  # noqa: E501
        :type: str
        """
        if status is None:
            raise ValueError("Invalid value for `status`, must not be `None`")  # noqa: E501

        self._status = status

    @property
    def total_hits(self):
        """Gets the total_hits of this FYFSkillResponse.  # noqa: E501


        :return: The total_hits of this FYFSkillResponse.  # noqa: E501
        :rtype: int
        """
        return self._total_hits

    @total_hits.setter
    def total_hits(self, total_hits):
        """Sets the total_hits of this FYFSkillResponse.


        :param total_hits: The total_hits of this FYFSkillResponse.  # noqa: E501
        :type: int
        """

        self._total_hits = total_hits

    @property
    def data(self):
        """Gets the data of this FYFSkillResponse.  # noqa: E501


        :return: The data of this FYFSkillResponse.  # noqa: E501
        :rtype: SkillResults
        """
        return self._data

    @data.setter
    def data(self, data):
        """Sets the data of this FYFSkillResponse.


        :param data: The data of this FYFSkillResponse.  # noqa: E501
        :type: SkillResults
        """

        self._data = data

    @property
    def message(self):
        """Gets the message of this FYFSkillResponse.  # noqa: E501


        :return: The message of this FYFSkillResponse.  # noqa: E501
        :rtype: str
        """
        return self._message

    @message.setter
    def message(self, message):
        """Sets the message of this FYFSkillResponse.


        :param message: The message of this FYFSkillResponse.  # noqa: E501
        :type: str
        """

        self._message = message

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
        if issubclass(FYFSkillResponse, dict):
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
        if not isinstance(other, FYFSkillResponse):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
