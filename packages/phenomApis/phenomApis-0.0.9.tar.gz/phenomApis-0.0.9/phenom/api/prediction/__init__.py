# coding: utf-8

# flake8: noqa

"""
    prediction-api

    Prediction api   # noqa: E501

    
"""

from __future__ import absolute_import

# import apis into sdk package
from phenom.api.prediction.prediction_api import PredictionApi
# import ApiClient
# import models into sdk package
from phenom.api.prediction.models.bad_request import BadRequest
from phenom.api.prediction.models.error_response import ErrorResponse
from phenom.api.prediction.models.fyf_skill_request import FYFSkillRequest
from phenom.api.prediction.models.fyf_skill_response import FYFSkillResponse
from phenom.api.prediction.models.skill_result import SkillResult
from phenom.api.prediction.models.skill_results import SkillResults
