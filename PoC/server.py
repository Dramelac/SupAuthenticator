from PoC.authenticator import Authenticator
import base64
import random


class ServerAuthenticator(Authenticator):

    def __init__(self, key=None):
        self.__key = key if key is not None else self.key_generator()
        super().__init__(self.__key)

    def export_key(self):
        return base64.b64encode(self.__key)

    @staticmethod
    def key_generator():
        return "".join(random.randint(0, 255) for _ in range(16))
