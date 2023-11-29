# coding: utf-8

"""
    recommendations-api

    Profile Based Job recommendations, Similar Jobs and Near By Jobs  # noqa: E501

    
"""

import pprint
import re  # noqa: F401

import six

class SimilarJobsResponseDataSimilarJobs(object):
    """
    Attributes:
      swagger_types (dict): The key is attribute name
                            and the value is attribute type.
      attribute_map (dict): The key is attribute name
                            and the value is json key in definition.
    """
    swagger_types = {
        'title': 'str',
        'job_id': 'str',
        'category': 'str',
        'location': 'str',
        'description': 'str'
    }

    attribute_map = {
        'title': 'title',
        'job_id': 'jobId',
        'category': 'category',
        'location': 'location',
        'description': 'description'
    }

    def __init__(self, title=None, job_id=None, category=None, location=None, description=None):  # noqa: E501
        """SimilarJobsResponseDataSimilarJobs - a model defined in Swagger"""  # noqa: E501
        self._title = None
        self._job_id = None
        self._category = None
        self._location = None
        self._description = None
        self.discriminator = None
        if title is not None:
            self.title = title
        if job_id is not None:
            self.job_id = job_id
        if category is not None:
            self.category = category
        if location is not None:
            self.location = location
        if description is not None:
            self.description = description

    @property
    def title(self):
        """Gets the title of this SimilarJobsResponseDataSimilarJobs.  # noqa: E501


        :return: The title of this SimilarJobsResponseDataSimilarJobs.  # noqa: E501
        :rtype: str
        """
        return self._title

    @title.setter
    def title(self, title):
        """Sets the title of this SimilarJobsResponseDataSimilarJobs.


        :param title: The title of this SimilarJobsResponseDataSimilarJobs.  # noqa: E501
        :type: str
        """

        self._title = title

    @property
    def job_id(self):
        """Gets the job_id of this SimilarJobsResponseDataSimilarJobs.  # noqa: E501


        :return: The job_id of this SimilarJobsResponseDataSimilarJobs.  # noqa: E501
        :rtype: str
        """
        return self._job_id

    @job_id.setter
    def job_id(self, job_id):
        """Sets the job_id of this SimilarJobsResponseDataSimilarJobs.


        :param job_id: The job_id of this SimilarJobsResponseDataSimilarJobs.  # noqa: E501
        :type: str
        """

        self._job_id = job_id

    @property
    def category(self):
        """Gets the category of this SimilarJobsResponseDataSimilarJobs.  # noqa: E501


        :return: The category of this SimilarJobsResponseDataSimilarJobs.  # noqa: E501
        :rtype: str
        """
        return self._category

    @category.setter
    def category(self, category):
        """Sets the category of this SimilarJobsResponseDataSimilarJobs.


        :param category: The category of this SimilarJobsResponseDataSimilarJobs.  # noqa: E501
        :type: str
        """

        self._category = category

    @property
    def location(self):
        """Gets the location of this SimilarJobsResponseDataSimilarJobs.  # noqa: E501


        :return: The location of this SimilarJobsResponseDataSimilarJobs.  # noqa: E501
        :rtype: str
        """
        return self._location

    @location.setter
    def location(self, location):
        """Sets the location of this SimilarJobsResponseDataSimilarJobs.


        :param location: The location of this SimilarJobsResponseDataSimilarJobs.  # noqa: E501
        :type: str
        """

        self._location = location

    @property
    def description(self):
        """Gets the description of this SimilarJobsResponseDataSimilarJobs.  # noqa: E501


        :return: The description of this SimilarJobsResponseDataSimilarJobs.  # noqa: E501
        :rtype: str
        """
        return self._description

    @description.setter
    def description(self, description):
        """Sets the description of this SimilarJobsResponseDataSimilarJobs.


        :param description: The description of this SimilarJobsResponseDataSimilarJobs.  # noqa: E501
        :type: str
        """

        self._description = description

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
        if issubclass(SimilarJobsResponseDataSimilarJobs, dict):
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
        if not isinstance(other, SimilarJobsResponseDataSimilarJobs):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
