# coding: utf-8

"""
    job-parser-api

    The process of extracting important information from the raw job description is called Job Parsing. This information can include things like job titles, required skills, required experience, job duties, and qualifications.  # noqa: E501

    
"""

import pprint
import re  # noqa: F401

import six

class JobResponse(object):
    """
    Attributes:
      swagger_types (dict): The key is attribute name
                            and the value is attribute type.
      attribute_map (dict): The key is attribute name
                            and the value is json key in definition.
    """
    swagger_types = {
        'skills': 'list[str]',
        'skill_ranking': 'list[object]',
        'job_teaser': 'str',
        'job_experience': 'object',
        'language': 'str',
        'requirement_sentences': 'list[str]',
        'responsibility_sentences': 'list[str]',
        'experience_sentences': 'list[str]',
        'soft_skills_sentences': 'list[str]',
        'skills_sentences': 'list[str]',
        'education_sentences': 'list[str]',
        'job_zone': 'str',
        'job_preferred_languages': 'str',
        'cleaned_title': 'str',
        'onet': 'list[object]',
        'job_type_fields': 'object',
        'language_fullform': 'str',
        'job_domain': 'str',
        'education_fields': 'list[str]',
        'status': 'int'
    }

    attribute_map = {
        'skills': 'skills',
        'skill_ranking': 'skill_ranking',
        'job_teaser': 'job_teaser',
        'job_experience': 'job_experience',
        'language': 'language',
        'requirement_sentences': 'requirement_sentences',
        'responsibility_sentences': 'responsibility_sentences',
        'experience_sentences': 'experience_sentences',
        'soft_skills_sentences': 'soft_skills_sentences',
        'skills_sentences': 'skills_sentences',
        'education_sentences': 'education_sentences',
        'job_zone': 'job_zone',
        'job_preferred_languages': 'job_preferred_languages',
        'cleaned_title': 'cleaned_title',
        'onet': 'onet',
        'job_type_fields': 'job_type_fields',
        'language_fullform': 'language_fullform',
        'job_domain': 'job_domain',
        'education_fields': 'education_fields',
        'status': 'status'
    }

    def __init__(self, skills=None, skill_ranking=None, job_teaser=None, job_experience=None, language=None, requirement_sentences=None, responsibility_sentences=None, experience_sentences=None, soft_skills_sentences=None, skills_sentences=None, education_sentences=None, job_zone=None, job_preferred_languages=None, cleaned_title=None, onet=None, job_type_fields=None, language_fullform=None, job_domain=None, education_fields=None, status=None):  # noqa: E501
        """JobResponse - a model defined in Swagger"""  # noqa: E501
        self._skills = None
        self._skill_ranking = None
        self._job_teaser = None
        self._job_experience = None
        self._language = None
        self._requirement_sentences = None
        self._responsibility_sentences = None
        self._experience_sentences = None
        self._soft_skills_sentences = None
        self._skills_sentences = None
        self._education_sentences = None
        self._job_zone = None
        self._job_preferred_languages = None
        self._cleaned_title = None
        self._onet = None
        self._job_type_fields = None
        self._language_fullform = None
        self._job_domain = None
        self._education_fields = None
        self._status = None
        self.discriminator = None
        if skills is not None:
            self.skills = skills
        if skill_ranking is not None:
            self.skill_ranking = skill_ranking
        if job_teaser is not None:
            self.job_teaser = job_teaser
        if job_experience is not None:
            self.job_experience = job_experience
        if language is not None:
            self.language = language
        if requirement_sentences is not None:
            self.requirement_sentences = requirement_sentences
        if responsibility_sentences is not None:
            self.responsibility_sentences = responsibility_sentences
        if experience_sentences is not None:
            self.experience_sentences = experience_sentences
        if soft_skills_sentences is not None:
            self.soft_skills_sentences = soft_skills_sentences
        if skills_sentences is not None:
            self.skills_sentences = skills_sentences
        if education_sentences is not None:
            self.education_sentences = education_sentences
        if job_zone is not None:
            self.job_zone = job_zone
        if job_preferred_languages is not None:
            self.job_preferred_languages = job_preferred_languages
        if cleaned_title is not None:
            self.cleaned_title = cleaned_title
        if onet is not None:
            self.onet = onet
        if job_type_fields is not None:
            self.job_type_fields = job_type_fields
        if language_fullform is not None:
            self.language_fullform = language_fullform
        if job_domain is not None:
            self.job_domain = job_domain
        if education_fields is not None:
            self.education_fields = education_fields
        if status is not None:
            self.status = status

    @property
    def skills(self):
        """Gets the skills of this JobResponse.  # noqa: E501


        :return: The skills of this JobResponse.  # noqa: E501
        :rtype: list[str]
        """
        return self._skills

    @skills.setter
    def skills(self, skills):
        """Sets the skills of this JobResponse.


        :param skills: The skills of this JobResponse.  # noqa: E501
        :type: list[str]
        """

        self._skills = skills

    @property
    def skill_ranking(self):
        """Gets the skill_ranking of this JobResponse.  # noqa: E501


        :return: The skill_ranking of this JobResponse.  # noqa: E501
        :rtype: list[object]
        """
        return self._skill_ranking

    @skill_ranking.setter
    def skill_ranking(self, skill_ranking):
        """Sets the skill_ranking of this JobResponse.


        :param skill_ranking: The skill_ranking of this JobResponse.  # noqa: E501
        :type: list[object]
        """

        self._skill_ranking = skill_ranking

    @property
    def job_teaser(self):
        """Gets the job_teaser of this JobResponse.  # noqa: E501


        :return: The job_teaser of this JobResponse.  # noqa: E501
        :rtype: str
        """
        return self._job_teaser

    @job_teaser.setter
    def job_teaser(self, job_teaser):
        """Sets the job_teaser of this JobResponse.


        :param job_teaser: The job_teaser of this JobResponse.  # noqa: E501
        :type: str
        """

        self._job_teaser = job_teaser

    @property
    def job_experience(self):
        """Gets the job_experience of this JobResponse.  # noqa: E501


        :return: The job_experience of this JobResponse.  # noqa: E501
        :rtype: object
        """
        return self._job_experience

    @job_experience.setter
    def job_experience(self, job_experience):
        """Sets the job_experience of this JobResponse.


        :param job_experience: The job_experience of this JobResponse.  # noqa: E501
        :type: object
        """

        self._job_experience = job_experience

    @property
    def language(self):
        """Gets the language of this JobResponse.  # noqa: E501


        :return: The language of this JobResponse.  # noqa: E501
        :rtype: str
        """
        return self._language

    @language.setter
    def language(self, language):
        """Sets the language of this JobResponse.


        :param language: The language of this JobResponse.  # noqa: E501
        :type: str
        """

        self._language = language

    @property
    def requirement_sentences(self):
        """Gets the requirement_sentences of this JobResponse.  # noqa: E501


        :return: The requirement_sentences of this JobResponse.  # noqa: E501
        :rtype: list[str]
        """
        return self._requirement_sentences

    @requirement_sentences.setter
    def requirement_sentences(self, requirement_sentences):
        """Sets the requirement_sentences of this JobResponse.


        :param requirement_sentences: The requirement_sentences of this JobResponse.  # noqa: E501
        :type: list[str]
        """

        self._requirement_sentences = requirement_sentences

    @property
    def responsibility_sentences(self):
        """Gets the responsibility_sentences of this JobResponse.  # noqa: E501


        :return: The responsibility_sentences of this JobResponse.  # noqa: E501
        :rtype: list[str]
        """
        return self._responsibility_sentences

    @responsibility_sentences.setter
    def responsibility_sentences(self, responsibility_sentences):
        """Sets the responsibility_sentences of this JobResponse.


        :param responsibility_sentences: The responsibility_sentences of this JobResponse.  # noqa: E501
        :type: list[str]
        """

        self._responsibility_sentences = responsibility_sentences

    @property
    def experience_sentences(self):
        """Gets the experience_sentences of this JobResponse.  # noqa: E501


        :return: The experience_sentences of this JobResponse.  # noqa: E501
        :rtype: list[str]
        """
        return self._experience_sentences

    @experience_sentences.setter
    def experience_sentences(self, experience_sentences):
        """Sets the experience_sentences of this JobResponse.


        :param experience_sentences: The experience_sentences of this JobResponse.  # noqa: E501
        :type: list[str]
        """

        self._experience_sentences = experience_sentences

    @property
    def soft_skills_sentences(self):
        """Gets the soft_skills_sentences of this JobResponse.  # noqa: E501


        :return: The soft_skills_sentences of this JobResponse.  # noqa: E501
        :rtype: list[str]
        """
        return self._soft_skills_sentences

    @soft_skills_sentences.setter
    def soft_skills_sentences(self, soft_skills_sentences):
        """Sets the soft_skills_sentences of this JobResponse.


        :param soft_skills_sentences: The soft_skills_sentences of this JobResponse.  # noqa: E501
        :type: list[str]
        """

        self._soft_skills_sentences = soft_skills_sentences

    @property
    def skills_sentences(self):
        """Gets the skills_sentences of this JobResponse.  # noqa: E501


        :return: The skills_sentences of this JobResponse.  # noqa: E501
        :rtype: list[str]
        """
        return self._skills_sentences

    @skills_sentences.setter
    def skills_sentences(self, skills_sentences):
        """Sets the skills_sentences of this JobResponse.


        :param skills_sentences: The skills_sentences of this JobResponse.  # noqa: E501
        :type: list[str]
        """

        self._skills_sentences = skills_sentences

    @property
    def education_sentences(self):
        """Gets the education_sentences of this JobResponse.  # noqa: E501


        :return: The education_sentences of this JobResponse.  # noqa: E501
        :rtype: list[str]
        """
        return self._education_sentences

    @education_sentences.setter
    def education_sentences(self, education_sentences):
        """Sets the education_sentences of this JobResponse.


        :param education_sentences: The education_sentences of this JobResponse.  # noqa: E501
        :type: list[str]
        """

        self._education_sentences = education_sentences

    @property
    def job_zone(self):
        """Gets the job_zone of this JobResponse.  # noqa: E501


        :return: The job_zone of this JobResponse.  # noqa: E501
        :rtype: str
        """
        return self._job_zone

    @job_zone.setter
    def job_zone(self, job_zone):
        """Sets the job_zone of this JobResponse.


        :param job_zone: The job_zone of this JobResponse.  # noqa: E501
        :type: str
        """

        self._job_zone = job_zone

    @property
    def job_preferred_languages(self):
        """Gets the job_preferred_languages of this JobResponse.  # noqa: E501


        :return: The job_preferred_languages of this JobResponse.  # noqa: E501
        :rtype: str
        """
        return self._job_preferred_languages

    @job_preferred_languages.setter
    def job_preferred_languages(self, job_preferred_languages):
        """Sets the job_preferred_languages of this JobResponse.


        :param job_preferred_languages: The job_preferred_languages of this JobResponse.  # noqa: E501
        :type: str
        """

        self._job_preferred_languages = job_preferred_languages

    @property
    def cleaned_title(self):
        """Gets the cleaned_title of this JobResponse.  # noqa: E501


        :return: The cleaned_title of this JobResponse.  # noqa: E501
        :rtype: str
        """
        return self._cleaned_title

    @cleaned_title.setter
    def cleaned_title(self, cleaned_title):
        """Sets the cleaned_title of this JobResponse.


        :param cleaned_title: The cleaned_title of this JobResponse.  # noqa: E501
        :type: str
        """

        self._cleaned_title = cleaned_title

    @property
    def onet(self):
        """Gets the onet of this JobResponse.  # noqa: E501


        :return: The onet of this JobResponse.  # noqa: E501
        :rtype: list[object]
        """
        return self._onet

    @onet.setter
    def onet(self, onet):
        """Sets the onet of this JobResponse.


        :param onet: The onet of this JobResponse.  # noqa: E501
        :type: list[object]
        """

        self._onet = onet

    @property
    def job_type_fields(self):
        """Gets the job_type_fields of this JobResponse.  # noqa: E501


        :return: The job_type_fields of this JobResponse.  # noqa: E501
        :rtype: object
        """
        return self._job_type_fields

    @job_type_fields.setter
    def job_type_fields(self, job_type_fields):
        """Sets the job_type_fields of this JobResponse.


        :param job_type_fields: The job_type_fields of this JobResponse.  # noqa: E501
        :type: object
        """

        self._job_type_fields = job_type_fields

    @property
    def language_fullform(self):
        """Gets the language_fullform of this JobResponse.  # noqa: E501


        :return: The language_fullform of this JobResponse.  # noqa: E501
        :rtype: str
        """
        return self._language_fullform

    @language_fullform.setter
    def language_fullform(self, language_fullform):
        """Sets the language_fullform of this JobResponse.


        :param language_fullform: The language_fullform of this JobResponse.  # noqa: E501
        :type: str
        """

        self._language_fullform = language_fullform

    @property
    def job_domain(self):
        """Gets the job_domain of this JobResponse.  # noqa: E501


        :return: The job_domain of this JobResponse.  # noqa: E501
        :rtype: str
        """
        return self._job_domain

    @job_domain.setter
    def job_domain(self, job_domain):
        """Sets the job_domain of this JobResponse.


        :param job_domain: The job_domain of this JobResponse.  # noqa: E501
        :type: str
        """

        self._job_domain = job_domain

    @property
    def education_fields(self):
        """Gets the education_fields of this JobResponse.  # noqa: E501


        :return: The education_fields of this JobResponse.  # noqa: E501
        :rtype: list[str]
        """
        return self._education_fields

    @education_fields.setter
    def education_fields(self, education_fields):
        """Sets the education_fields of this JobResponse.


        :param education_fields: The education_fields of this JobResponse.  # noqa: E501
        :type: list[str]
        """

        self._education_fields = education_fields

    @property
    def status(self):
        """Gets the status of this JobResponse.  # noqa: E501


        :return: The status of this JobResponse.  # noqa: E501
        :rtype: int
        """
        return self._status

    @status.setter
    def status(self, status):
        """Sets the status of this JobResponse.


        :param status: The status of this JobResponse.  # noqa: E501
        :type: int
        """

        self._status = status

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
        if issubclass(JobResponse, dict):
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
        if not isinstance(other, JobResponse):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
