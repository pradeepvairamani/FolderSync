import requests
import json
import base64

PP_AUTH_URL = 'https://service.projectplace.com/oauth2/access_token?'
PP_CLIENT_ID = '4b61c9d7a5eb5c9463742118b909d808'
PP_CLIENT_SECRET = '7b3a46f245b3037a44703a3852cb88549658ccf5'
PP_PASSWORD = 'hgb67dgsf9lk0odjdhsn2n12'
PP_API_ENDPOINT = 'https://api.projectplace.com/1/'


def get_base64_password(password):
    key = PP_CLIENT_ID+':'+PP_PASSWORD
    return base64.b64encode(key)


def oauth2_access_token_request(email, password, secret):
        args = {
            'email': email,
            'password': password,
            'grant_type': 'password'
        }

        headers = {'Authorization': 'Basic {0}'.format(secret)}

        response = requests.post('https://service.projectplace.com/oauth2/access_token', args, headers=headers)

        return _handle_auth_response(response)


def _oauth2_request_token_request(refresh_token):
        args = {
            'client_id': PP_CLIENT_ID,
            'client_secret': PP_CLIENT_SECRET,
            'refresh_token': refresh_token,
            'grant_type': 'refresh_token'
        }

        response = requests.post('https://service.projectplace.com/oauth2/access_token', args)

        return _handle_auth_response(response)


def _handle_auth_response(response):
    result = json.loads(response.text)

    #Handle errors
    return PPClient(result['access_token'], result['refresh_token'])


class PPClient(object):

    def __init__(self, access_token=None, refresh_token=None):
        self.access_token = access_token
        self.refresh_token = refresh_token
        self._client_id = PP_CLIENT_ID
        self._client_secret = PP_CLIENT_SECRET
        self._password = PP_PASSWORD

    @property
    def headers(self):
        return {'Authorization': 'Bearer {0}'.format(self.access_token)}

    def request(self, method, resource, params=None, data=None, headers=None, try_refresh=True, **kwargs):

            if headers:
                headers = dict(headers)
            else:
                headers = self.headers

            url = 'https://api.projectplace.com/1/%s' % resource

            response = requests.request(method, url, params=params, data=data, headers=headers, **kwargs)

            if response.status_code != 200 and self.refresh():
                return self.request(method, resource, params, data, headers, try_refresh=False, **kwargs)

            # _check_for_errors(response)

            return json.loads(response.text)

    def refresh(self):
        if not self.refresh_token:
            return False

        result = self._oauth2_request_token_request(self.refresh_token)

        self._access_token = result['access_token']
        self._refresh_token = result['refresh_token']
        return True
