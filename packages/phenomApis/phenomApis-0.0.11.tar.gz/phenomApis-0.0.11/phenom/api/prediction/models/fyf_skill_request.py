# coding: utf-8

"""
    prediction-api

    Prediction api   # noqa: E501

    
"""

import pprint
import re  # noqa: F401

import six

class FYFSkillRequest(object):
    """
    Attributes:
      swagger_types (dict): The key is attribute name
                            and the value is attribute type.
      attribute_map (dict): The key is attribute name
                            and the value is json key in definition.
    """
    swagger_types = {
        'titles': 'list[str]',
        'categories': 'list[str]',
        'skills': 'list[str]',
        'size': 'int',
        'source': 'str'
    }

    attribute_map = {
        'titles': 'titles',
        'categories': 'categories',
        'skills': 'skills',
        'size': 'size',
        'source': 'source'
    }

    def __init__(self, titles=None, categories=None, skills=None, size=10, source=None):  # noqa: E501
        """FYFSkillRequest - a model defined in Swagger"""  # noqa: E501
        self._titles = None
        self._categories = None
        self._skills = None
        self._size = None
        self._source = None
        self.discriminator = None
        if titles is not None:
            self.titles = titles
        if categories is not None:
            self.categories = categories
        if skills is not None:
            self.skills = skills
        if size is not None:
            self.size = size
        if source is not None:
            self.source = source

    @property
    def titles(self):
        """Gets the titles of this FYFSkillRequest.  # noqa: E501


        :return: The titles of this FYFSkillRequest.  # noqa: E501
        :rtype: list[str]
        """
        return self._titles

    @titles.setter
    def titles(self, titles):
        """Sets the titles of this FYFSkillRequest.


        :param titles: The titles of this FYFSkillRequest.  # noqa: E501
        :type: list[str]
        """

        self._titles = titles

    @property
    def categories(self):
        """Gets the categories of this FYFSkillRequest.  # noqa: E501


        :return: The categories of this FYFSkillRequest.  # noqa: E501
        :rtype: list[str]
        """
        return self._categories

    @categories.setter
    def categories(self, categories):
        """Sets the categories of this FYFSkillRequest.


        :param categories: The categories of this FYFSkillRequest.  # noqa: E501
        :type: list[str]
        """

        self._categories = categories

    @property
    def skills(self):
        """Gets the skills of this FYFSkillRequest.  # noqa: E501


        :return: The skills of this FYFSkillRequest.  # noqa: E501
        :rtype: list[str]
        """
        return self._skills

    @skills.setter
    def skills(self, skills):
        """Sets the skills of this FYFSkillRequest.


        :param skills: The skills of this FYFSkillRequest.  # noqa: E501
        :type: list[str]
        """

        self._skills = skills

    @property
    def size(self):
        """Gets the size of this FYFSkillRequest.  # noqa: E501


        :return: The size of this FYFSkillRequest.  # noqa: E501
        :rtype: int
        """
        return self._size

    @size.setter
    def size(self, size):
        """Sets the size of this FYFSkillRequest.


        :param size: The size of this FYFSkillRequest.  # noqa: E501
        :type: int
        """

        self._size = size

    @property
    def source(self):
        """Gets the source of this FYFSkillRequest.  # noqa: E501


        :return: The source of this FYFSkillRequest.  # noqa: E501
        :rtype: str
        """
        return self._source

    @source.setter
    def source(self, source):
        """Sets the source of this FYFSkillRequest.


        :param source: The source of this FYFSkillRequest.  # noqa: E501
        :type: str
        """

        self._source = source

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
        if issubclass(FYFSkillRequest, dict):
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
        if not isinstance(other, FYFSkillRequest):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
