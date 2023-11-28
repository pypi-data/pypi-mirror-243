# coding: utf-8

"""
    ex-search-api

    These APIs helps to search and suggest based on keyword among employee profiles  # noqa: E501

    
"""

import pprint
import re  # noqa: F401

import six

class CommonNode(object):
    """
    Attributes:
      swagger_types (dict): The key is attribute name
                            and the value is attribute type.
      attribute_map (dict): The key is attribute name
                            and the value is json key in definition.
    """
    swagger_types = {
        'ref_num': 'str',
        'user_id': 'str',
        'user_type': 'str'
    }

    attribute_map = {
        'ref_num': 'refNum',
        'user_id': 'userId',
        'user_type': 'userType'
    }

    def __init__(self, ref_num=None, user_id=None, user_type=None):  # noqa: E501
        """CommonNode - a model defined in Swagger"""  # noqa: E501
        self._ref_num = None
        self._user_id = None
        self._user_type = None
        self.discriminator = None
        if ref_num is not None:
            self.ref_num = ref_num
        if user_id is not None:
            self.user_id = user_id
        if user_type is not None:
            self.user_type = user_type

    @property
    def ref_num(self):
        """Gets the ref_num of this CommonNode.  # noqa: E501


        :return: The ref_num of this CommonNode.  # noqa: E501
        :rtype: str
        """
        return self._ref_num

    @ref_num.setter
    def ref_num(self, ref_num):
        """Sets the ref_num of this CommonNode.


        :param ref_num: The ref_num of this CommonNode.  # noqa: E501
        :type: str
        """

        self._ref_num = ref_num

    @property
    def user_id(self):
        """Gets the user_id of this CommonNode.  # noqa: E501


        :return: The user_id of this CommonNode.  # noqa: E501
        :rtype: str
        """
        return self._user_id

    @user_id.setter
    def user_id(self, user_id):
        """Sets the user_id of this CommonNode.


        :param user_id: The user_id of this CommonNode.  # noqa: E501
        :type: str
        """

        self._user_id = user_id

    @property
    def user_type(self):
        """Gets the user_type of this CommonNode.  # noqa: E501


        :return: The user_type of this CommonNode.  # noqa: E501
        :rtype: str
        """
        return self._user_type

    @user_type.setter
    def user_type(self, user_type):
        """Sets the user_type of this CommonNode.


        :param user_type: The user_type of this CommonNode.  # noqa: E501
        :type: str
        """

        self._user_type = user_type

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
        if issubclass(CommonNode, dict):
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
        if not isinstance(other, CommonNode):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
