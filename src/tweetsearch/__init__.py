from .get_bearer_token import *
import requests


# import time


class TweetSearch(object):
    request_limit = 450
    request_horizon = 900  # seconds - == 15m

    def __init__(self, token, api_url="https://api.twitter.com/1.1/search/tweets.json", **kwargs):
        self.api_url = api_url
        self.token = token

        if type(token) is tuple:
            self.token = get_bearer_token(token[0], token[1])

        if self.token is dict:
            raise ValueError("There was an error getting your Bearer Token: {}".format(self.token))

        self.auth_header = bearer_auth_header(self.token)
        self.last_tweet = None
        self.last_query = None

        if 'last_tweet' in kwargs:
            self.last_tweet = kwargs['last_tweet']

        self.requests = []

    def search(self, query, **kwargs):
        params = kwargs.copy()
        params['q'] = query

        if 'result_type' not in params:
            params['result_type'] = 'recent'
        if 'count' not in params:
            params['count'] = 50

        # self.requests.append(time.time())

        # print(self.auth_header)
        print(params)
        response = requests.get(self.api_url, headers=self.auth_header, params=params).json()
        if 'statuses' not in response:
            raise PermissionError(response)

        max_id = 0
        for tweet in response['statuses']:
            if int(tweet['id']) > max_id:
                max_id = int(tweet['id'])

        if max_id > 0:
            self.last_tweet = max_id

        self.last_query = (query, params)
        return response['statuses']

    def repeat_search(self, query=None, last_tweet=None):
        if query is None:
            query = self.last_query
        if last_tweet is None:
            last_tweet = self.last_tweet

        params = query[1]
        params['since_id'] = last_tweet
        # print(params)
        return self.search(query=query[0], **params)
