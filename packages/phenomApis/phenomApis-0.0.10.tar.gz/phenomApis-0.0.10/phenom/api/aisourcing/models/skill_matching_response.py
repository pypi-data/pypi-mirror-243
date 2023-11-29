# coding: utf-8

"""
    aisourcing-api

    AI Matching apis   # noqa: E501

    
"""

import pprint
import re  # noqa: F401

import six

class SkillMatchingResponse(object):
    """
    Attributes:
      swagger_types (dict): The key is attribute name
                            and the value is attribute type.
      attribute_map (dict): The key is attribute name
                            and the value is json key in definition.
    """
    swagger_types = {
        'matching_skills': 'list[str]',
        'matching_skills_count': 'int'
    }

    attribute_map = {
        'matching_skills': 'matchingSkills',
        'matching_skills_count': 'matchingSkillsCount'
    }

    def __init__(self, matching_skills=None, matching_skills_count=None):  # noqa: E501
        """SkillMatchingResponse - a model defined in Swagger"""  # noqa: E501
        self._matching_skills = None
        self._matching_skills_count = None
        self.discriminator = None
        if matching_skills is not None:
            self.matching_skills = matching_skills
        if matching_skills_count is not None:
            self.matching_skills_count = matching_skills_count

    @property
    def matching_skills(self):
        """Gets the matching_skills of this SkillMatchingResponse.  # noqa: E501


        :return: The matching_skills of this SkillMatchingResponse.  # noqa: E501
        :rtype: list[str]
        """
        return self._matching_skills

    @matching_skills.setter
    def matching_skills(self, matching_skills):
        """Sets the matching_skills of this SkillMatchingResponse.


        :param matching_skills: The matching_skills of this SkillMatchingResponse.  # noqa: E501
        :type: list[str]
        """

        self._matching_skills = matching_skills

    @property
    def matching_skills_count(self):
        """Gets the matching_skills_count of this SkillMatchingResponse.  # noqa: E501


        :return: The matching_skills_count of this SkillMatchingResponse.  # noqa: E501
        :rtype: int
        """
        return self._matching_skills_count

    @matching_skills_count.setter
    def matching_skills_count(self, matching_skills_count):
        """Sets the matching_skills_count of this SkillMatchingResponse.


        :param matching_skills_count: The matching_skills_count of this SkillMatchingResponse.  # noqa: E501
        :type: int
        """

        self._matching_skills_count = matching_skills_count

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
        if issubclass(SkillMatchingResponse, dict):
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
        if not isinstance(other, SkillMatchingResponse):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
