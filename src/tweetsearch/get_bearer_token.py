import requests
import base64


def get_bearer_token(api_consumer_key, api_consumer_secret, api_url='https://api.twitter.com/oauth2/token'):
    auth_header = "{}:{}".format(api_consumer_key, api_consumer_secret)
    print(auth_header)
    auth_header = base64.b64encode(auth_header.encode('ascii'))
    auth_header = {'Authorization': "Basic {}".format(auth_header.decode())}

    print(auth_header)

    response = requests.post(
        api_url,
        headers=auth_header,
        data={'grant_type': 'client_credentials'})

    print(response.content)

    rdict = response.json()
    if 'access_token' not in rdict:
        return rdict
    return rdict['access_token']


def bearer_auth_header(bearer_access_token):
    return {'Authorization': 'Bearer {}'.format(bearer_access_token)}
