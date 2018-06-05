import base64
import random
import time

from SupAuthenticator.tools.authenticator import Authenticator


class ServerAuthenticator(Authenticator):

    def __init__(self, key=None):
        self.__key = base64.standard_b64decode(key) if key is not None else self.__key_generator()
        super().__init__(self.__key)

    def export_key(self):
        return base64.b64encode(self.__key)

    @staticmethod
    def __key_generator():
        return b"".join(bytes([random.randint(0, 255)]) for _ in range(16))

    def get_previous_token(self):
        previous_time = time.time() - self._token_time
        previous_time -= previous_time % self._token_time
        return self._build_token(previous_time)
