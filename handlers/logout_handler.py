from agar.sessions import SessionRequestHandler
from restler.serializers import json_response


class LogoutHandler(SessionRequestHandler):
    def _logout(self):
        if 'user_key' in self.session:
            del self.session['user_key']
        if 'distributor' in self.session:
            del self.session['distributor']
        if 'state' in self.session:
            del self.session['state']
        if 'is_administrator' in self.session:
            del self.session['is_administrator']
        json_response(self.response, {'message': 'Successful Logout'}, status_code=200)

    def get(self):
        self._logout()

    def post(self):
        self._logout()
