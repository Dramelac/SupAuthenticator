from PoC.authenticator import Authenticator
import base64
import random
import time


class ServerAuthenticator(Authenticator):

    def __init__(self, key=None):
        self.__key = key if key is not None else self.key_generator()
        super().__init__(self.__key)

    def export_key(self):
        return base64.b64encode(self.__key)

    @staticmethod
    def key_generator():
        return b"".join(bytes([random.randint(0, 255)]) for _ in range(16))

    def get_previous_token(self):
        previous_time = time.time()-60
        previous_time -= previous_time % 30
        return self._build_token(previous_time)
