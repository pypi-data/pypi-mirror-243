from phenom.commons.get_token import tokengeneration
from phenom.api.resumeparser.resume_parsing_api import ResumeParsingApi
from phenom.api.exsearch.employees_api import EmployeesApi
from phenom.api.prediction.prediction_api import PredictionApi
from phenom.api.aisourcing.ai_matching_api import AIMatchingApi
from phenom.api.search.jobs_api import JobsApi
from phenom.api.jobparser.job_parsing_api import JobParsingApi
from phenom.api.recomendation.recommendations_api import RecommendationsApi

class Authorization(object):
    def __init__(self, url, client_id, client_secret, gateway_url, apikey=None):
        self.url = url
        self.client_id = client_id
        self.client_secret = client_secret
        self.gateway_url = gateway_url
        self.apikey = apikey

    def token(self):
        return tokengeneration(self.url, self.client_id, self.client_secret)

    # resumeparser api methods
    def resumeparser(self):
        return ResumeParsingApi(self.token(), self.gateway_url, self.apikey)

    # employee search api methods
    def exsearch(self):
        return EmployeesApi(self.token(), self.gateway_url, self.apikey)

    # prediction api methods
    def prediction(self):
        return PredictionApi(self.token(), self.gateway_url, self.apikey)

    # ai-sourcing api methods
    def aisourcing(self):
        return AIMatchingApi(self.token(), self.gateway_url, self.apikey)

    # search api methods
    def search(self):
        return JobsApi(self.token(), self.gateway_url, self.apikey)

    # job-parser api methods
    def jobparser(self):
        return JobParsingApi(self.token(), self.gateway_url, self.apikey)

    # recommendation api methods
    def recommendation(self):
        return RecommendationsApi(self.token(), self.gateway_url, self.apikey)