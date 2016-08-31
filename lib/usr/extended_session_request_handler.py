from agar.sessions import SessionRequestHandler
import json
from ndb_mixins import KeyValidatorMixin, PagingListHandlerMixin


class ExtendedSessionRequestHandler(SessionRequestHandler, KeyValidatorMixin, PagingListHandlerMixin):
    def check_and_get_field(self, key, dictionary=None, abort_on_not_found=True):
        '''
        Checks to make sure key exists in dictionary, and if not, aborts the request.
        :param key: a unicode or string
        :param dictionary: a python dictionary. if none is provided, the request body is the assumed dictionary
        :return: value of key in dictionary
        '''
        if not dictionary:
            if self.request.body is not str('') and self.request.body is not None:
                dictionary = json.loads(self.request.body)
            else:
                self.abort(400, "body is empty")

        if type(dictionary) != dict:
            raise ValueError("You must supply a python dictionary as the second position arguement")
        if type(key) != str and type(key) != unicode:
            raise ValueError("You must supply a key with a type of string or type of unicode")

        value = dictionary.get(key)
        if value == None or value == '':
            if abort_on_not_found:
                self.abort(400, "required field {} not found".format(key))
            else:
                return value
        else:
            return value

    def check_and_get_query_param(self, query_param, abort_on_not_found=True):
        '''
        :param query_param: string
        :return: value of query param
        '''
        request = self.request
        value = request.get(query_param)
        if value == None or value == '':
            if abort_on_not_found:
                self.abort(400, "required query parameter {} not found".format(query_param))
            else:
                return value

        else:
            return value
