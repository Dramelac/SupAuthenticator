import base64
import hashlib
import time

from Crypto.Cipher import AES


class Authenticator:

    def __init__(self, key):
        self.__aes = AES.new(key)
        self.__cache_hash(key)
        self._token_time = 15

    def __cache_hash(self, key):
        self.__hash = hashlib.sha256(key).hexdigest()

    def generate_token(self):
        now_time = time.time()
        now_time -= now_time % self._token_time
        return self._build_token(now_time)

    def _build_token(self, time_selected):
        time_selected = int(time_selected)
        if self.__aes is None:
            raise Exception("Authenticator is not initialize")

        challenge = str(time_selected) + self.__hash
        hash_tmp = hashlib.sha256(challenge.encode("utf-8")).hexdigest()

        ciphered = self.__aes.encrypt(hash_tmp)
        base = base64.b64encode(ciphered)

        hash_tmp = hashlib.md5(base).hexdigest()

        result = ''.join([hash_tmp[i] for i in range(0, len(hash_tmp), 4)])
        return result.upper()
