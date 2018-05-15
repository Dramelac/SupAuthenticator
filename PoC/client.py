from PoC.authenticator import Authenticator
import base64


class ClientAuthenticator(Authenticator):

    def __init__(self, key):
        super().__init__(base64.b64decode(key))
