# coding: utf-8

"""
    ex-search-api

    These APIs helps to search and suggest based on keyword among employee profiles  # noqa: E501

    
"""

import pprint
import re  # noqa: F401

import six

class EmployeeNode(object):
    """
    Attributes:
      swagger_types (dict): The key is attribute name
                            and the value is attribute type.
      attribute_map (dict): The key is attribute name
                            and the value is json key in definition.
    """
    swagger_types = {
        'first_name': 'str',
        'skills': 'list[str]',
        'last_name': 'str',
        'candidate_id': 'str',
        'designation': 'str',
        'last_name_html': 'str',
        'first_name_html': 'str'
    }

    attribute_map = {
        'first_name': 'firstName',
        'skills': 'skills',
        'last_name': 'lastName',
        'candidate_id': 'candidateID',
        'designation': 'designation',
        'last_name_html': 'lastName_html',
        'first_name_html': 'firstName_html'
    }

    def __init__(self, first_name=None, skills=None, last_name=None, candidate_id=None, designation=None, last_name_html=None, first_name_html=None):  # noqa: E501
        """EmployeeNode - a model defined in Swagger"""  # noqa: E501
        self._first_name = None
        self._skills = None
        self._last_name = None
        self._candidate_id = None
        self._designation = None
        self._last_name_html = None
        self._first_name_html = None
        self.discriminator = None
        if first_name is not None:
            self.first_name = first_name
        if skills is not None:
            self.skills = skills
        if last_name is not None:
            self.last_name = last_name
        if candidate_id is not None:
            self.candidate_id = candidate_id
        if designation is not None:
            self.designation = designation
        if last_name_html is not None:
            self.last_name_html = last_name_html
        if first_name_html is not None:
            self.first_name_html = first_name_html

    @property
    def first_name(self):
        """Gets the first_name of this EmployeeNode.  # noqa: E501


        :return: The first_name of this EmployeeNode.  # noqa: E501
        :rtype: str
        """
        return self._first_name

    @first_name.setter
    def first_name(self, first_name):
        """Sets the first_name of this EmployeeNode.


        :param first_name: The first_name of this EmployeeNode.  # noqa: E501
        :type: str
        """

        self._first_name = first_name

    @property
    def skills(self):
        """Gets the skills of this EmployeeNode.  # noqa: E501


        :return: The skills of this EmployeeNode.  # noqa: E501
        :rtype: list[str]
        """
        return self._skills

    @skills.setter
    def skills(self, skills):
        """Sets the skills of this EmployeeNode.


        :param skills: The skills of this EmployeeNode.  # noqa: E501
        :type: list[str]
        """

        self._skills = skills

    @property
    def last_name(self):
        """Gets the last_name of this EmployeeNode.  # noqa: E501


        :return: The last_name of this EmployeeNode.  # noqa: E501
        :rtype: str
        """
        return self._last_name

    @last_name.setter
    def last_name(self, last_name):
        """Sets the last_name of this EmployeeNode.


        :param last_name: The last_name of this EmployeeNode.  # noqa: E501
        :type: str
        """

        self._last_name = last_name

    @property
    def candidate_id(self):
        """Gets the candidate_id of this EmployeeNode.  # noqa: E501


        :return: The candidate_id of this EmployeeNode.  # noqa: E501
        :rtype: str
        """
        return self._candidate_id

    @candidate_id.setter
    def candidate_id(self, candidate_id):
        """Sets the candidate_id of this EmployeeNode.


        :param candidate_id: The candidate_id of this EmployeeNode.  # noqa: E501
        :type: str
        """

        self._candidate_id = candidate_id

    @property
    def designation(self):
        """Gets the designation of this EmployeeNode.  # noqa: E501


        :return: The designation of this EmployeeNode.  # noqa: E501
        :rtype: str
        """
        return self._designation

    @designation.setter
    def designation(self, designation):
        """Sets the designation of this EmployeeNode.


        :param designation: The designation of this EmployeeNode.  # noqa: E501
        :type: str
        """

        self._designation = designation

    @property
    def last_name_html(self):
        """Gets the last_name_html of this EmployeeNode.  # noqa: E501


        :return: The last_name_html of this EmployeeNode.  # noqa: E501
        :rtype: str
        """
        return self._last_name_html

    @last_name_html.setter
    def last_name_html(self, last_name_html):
        """Sets the last_name_html of this EmployeeNode.


        :param last_name_html: The last_name_html of this EmployeeNode.  # noqa: E501
        :type: str
        """

        self._last_name_html = last_name_html

    @property
    def first_name_html(self):
        """Gets the first_name_html of this EmployeeNode.  # noqa: E501


        :return: The first_name_html of this EmployeeNode.  # noqa: E501
        :rtype: str
        """
        return self._first_name_html

    @first_name_html.setter
    def first_name_html(self, first_name_html):
        """Sets the first_name_html of this EmployeeNode.


        :param first_name_html: The first_name_html of this EmployeeNode.  # noqa: E501
        :type: str
        """

        self._first_name_html = first_name_html

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
        if issubclass(EmployeeNode, dict):
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
        if not isinstance(other, EmployeeNode):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
