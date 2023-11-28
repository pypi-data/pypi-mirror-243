# coding: utf-8

# flake8: noqa

"""
    recomendations-api

    Profile Based Job recomendations, Similar Jobs and Near By Jobs  # noqa: E501

    
"""

from __future__ import absolute_import

# import apis into sdk package
from phenom.api.recomendation.recommendations_api import RecommendationsApi
from phenom.commons.api_client import ApiClient
from phenom.commons.configuration import Configuration
# import models into sdk package
from phenom.api.recomendation.models.bad_request import BadRequest
from phenom.api.recomendation.models.error_response import ErrorResponse
from phenom.api.recomendation.models.job_node import JobNode
from phenom.api.recomendation.models.job_recommendation import JobRecommendation
from phenom.api.recomendation.models.near_by_jobs_response import NearByJobsResponse
from phenom.api.recomendation.models.near_by_jobs_response_data import NearByJobsResponseData
from phenom.api.recomendation.models.preferred_locations import PreferredLocations
from phenom.api.recomendation.models.preferred_locations_latlong import PreferredLocationsLatlong
from phenom.api.recomendation.models.profile_matching_response import ProfileMatchingResponse
from phenom.api.recomendation.models.profile_matching_response_jobs import ProfileMatchingResponseJobs
from phenom.api.recomendation.models.profile_matching_response_location_data import ProfileMatchingResponseLocationData
from phenom.api.recomendation.models.profile_matching_response_skill_gap import ProfileMatchingResponseSkillGap
from phenom.api.recomendation.models.similar_jobs_request import SimilarJobsRequest
from phenom.api.recomendation.models.similar_jobs_response import SimilarJobsResponse
from phenom.api.recomendation.models.similar_jobs_response_data import SimilarJobsResponseData
from phenom.api.recomendation.models.similar_jobs_response_data_similar_jobs import SimilarJobsResponseDataSimilarJobs
from phenom.api.recomendation.models.user_profile import UserProfile
