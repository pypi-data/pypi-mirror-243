# coding: utf-8

"""
    search-api

    These APIs helps to search and suggest based on keyword among available jobs  # noqa: E501

    
"""

import pprint
import re  # noqa: F401

import six

class RefineSearchRequestFacets(object):
    """
    Attributes:
      swagger_types (dict): The key is attribute name
                            and the value is attribute type.
      attribute_map (dict): The key is attribute name
                            and the value is json key in definition.
    """
    swagger_types = {
        'city': 'list[str]',
        'state': 'list[str]',
        'country': 'list[str]',
        'category': 'list[str]'
    }

    attribute_map = {
        'city': 'city',
        'state': 'state',
        'country': 'country',
        'category': 'category'
    }

    def __init__(self, city=None, state=None, country=None, category=None):  # noqa: E501
        """RefineSearchRequestFacets - a model defined in Swagger"""  # noqa: E501
        self._city = None
        self._state = None
        self._country = None
        self._category = None
        self.discriminator = None
        if city is not None:
            self.city = city
        if state is not None:
            self.state = state
        if country is not None:
            self.country = country
        if category is not None:
            self.category = category

    @property
    def city(self):
        """Gets the city of this RefineSearchRequestFacets.  # noqa: E501


        :return: The city of this RefineSearchRequestFacets.  # noqa: E501
        :rtype: list[str]
        """
        return self._city

    @city.setter
    def city(self, city):
        """Sets the city of this RefineSearchRequestFacets.


        :param city: The city of this RefineSearchRequestFacets.  # noqa: E501
        :type: list[str]
        """

        self._city = city

    @property
    def state(self):
        """Gets the state of this RefineSearchRequestFacets.  # noqa: E501


        :return: The state of this RefineSearchRequestFacets.  # noqa: E501
        :rtype: list[str]
        """
        return self._state

    @state.setter
    def state(self, state):
        """Sets the state of this RefineSearchRequestFacets.


        :param state: The state of this RefineSearchRequestFacets.  # noqa: E501
        :type: list[str]
        """

        self._state = state

    @property
    def country(self):
        """Gets the country of this RefineSearchRequestFacets.  # noqa: E501


        :return: The country of this RefineSearchRequestFacets.  # noqa: E501
        :rtype: list[str]
        """
        return self._country

    @country.setter
    def country(self, country):
        """Sets the country of this RefineSearchRequestFacets.


        :param country: The country of this RefineSearchRequestFacets.  # noqa: E501
        :type: list[str]
        """

        self._country = country

    @property
    def category(self):
        """Gets the category of this RefineSearchRequestFacets.  # noqa: E501


        :return: The category of this RefineSearchRequestFacets.  # noqa: E501
        :rtype: list[str]
        """
        return self._category

    @category.setter
    def category(self, category):
        """Sets the category of this RefineSearchRequestFacets.


        :param category: The category of this RefineSearchRequestFacets.  # noqa: E501
        :type: list[str]
        """

        self._category = category

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
        if issubclass(RefineSearchRequestFacets, dict):
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
        if not isinstance(other, RefineSearchRequestFacets):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
