# coding: utf-8

"""
    job-parser-api

    The process of extracting important information from the raw job description is called Job Parsing. This information can include things like job titles, required skills, required experience, job duties, and qualifications.  # noqa: E501

    
"""

import pprint
import re  # noqa: F401

import six

class Trigger400Response(object):
    """
    Attributes:
      swagger_types (dict): The key is attribute name
                            and the value is attribute type.
      attribute_map (dict): The key is attribute name
                            and the value is json key in definition.
    """
    swagger_types = {
        'response': 'Trigger400ResponseResponse'
    }

    attribute_map = {
        'response': 'response'
    }

    def __init__(self, response=None):  # noqa: E501
        """Trigger400Response - a model defined in Swagger"""  # noqa: E501
        self._response = None
        self.discriminator = None
        if response is not None:
            self.response = response

    @property
    def response(self):
        """Gets the response of this Trigger400Response.  # noqa: E501


        :return: The response of this Trigger400Response.  # noqa: E501
        :rtype: Trigger400ResponseResponse
        """
        return self._response

    @response.setter
    def response(self, response):
        """Sets the response of this Trigger400Response.


        :param response: The response of this Trigger400Response.  # noqa: E501
        :type: Trigger400ResponseResponse
        """

        self._response = response

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
        if issubclass(Trigger400Response, dict):
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
        if not isinstance(other, Trigger400Response):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
