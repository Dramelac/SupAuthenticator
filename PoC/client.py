import time

from PoC.authenticator import Authenticator
import base64


class ClientAuthenticator(Authenticator):

    def __init__(self, key):
        super().__init__(base64.b64decode(key))

    def __get_time_left(self):
        return self._token_time - (time.time() % self._token_time)

    def get_time_left(self):
        return int(self.__get_time_left())

    def get_percent_left(self):
        return int((100 * self.__get_time_left()) // self._token_time)
