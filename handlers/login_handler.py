from datetime import datetime
import json

from agar.sessions import SessionRequestHandler
from restler.serializers import json_response
import stormpath_api


class LoginHandler(SessionRequestHandler):
    def post(self):
        user = None
        body = json.loads(self.request.body)
        email = body.get('email', '').strip()
        password = body.get('password', '').strip()
        if email and password:
            user = stormpath_api.cloud_login(email, password)
        else:
            # Ensure that the request is not a forgery and that the user sending
            # this connect request is the expected user.
            state = body.get('state', '')
            if state == self.session.get('state'):
                id_token = body.get('id_token', None)
                access_token = body.get('access_token', None)
                code = body.get('code')
                user = stormpath_api.google_login(id_token, access_token, code)

        if user is None:
            result = {'message': 'Login Failed'}
            status_code = 400
        else:
            user.last_login = datetime.now()
            user.put()
            administrator = body.get('administrator', False)
            self.session['is_administrator'] = administrator is True and user.is_administrator
            self.session['user_key'] = user.key.urlsafe()
            if len(user.distributors) == 1:
                self.session['distributor'] = user.distributors[0].name
            result = {'message': 'Successful Login', 'user': {'key': user.key.urlsafe()}}
            status_code = 200

        json_response(self.response, result, status_code=status_code)
