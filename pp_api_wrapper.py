from authentication import oauth2_access_token_request, get_base64_password


class PPApi(object):

    def __init__(self, email, password):
        self._email = email
        self._password = password
        self.ppclient = oauth2_access_token_request(email, password, get_base64_password(password))

    def get_user_projects(self):
        return self.ppclient.request('get', 'user/me/projects.json')

    def download_file(self, document_id):
        return self.ppclient.request('get', 'document/{}'.format(document_id))

    def upload_file(self, document_id):
        return self.ppclient.request('put', '/document/{0}/upload.json'.format(document_id))
