import base64

from Crypto.Cipher import AES
import time
import hashlib


class Authenticator:

    def __init__(self, key):
        self.__aes = AES.new(key)
        self.__cache_hash(key)

    def __cache_hash(self, key):
        self.__hash = hashlib.sha256(key).hexdigest()

    def generate_token(self):
        now_time = time.time()
        now_time -= now_time % 30
        return self._build_token(now_time)

    def _build_token(self, time_selected):
        if self.__aes is None:
            raise Exception("Authenticator is not initialize")

        challenge = str(time_selected) + self.__hash
        hash_tmp = hashlib.sha256(challenge.encode("utf-8")).hexdigest()

        ciphered = self.__aes.encrypt(hash_tmp)
        base = base64.b64encode(ciphered)

        hash_tmp = hashlib.md5(base).hexdigest()

        result = ''.join([hash_tmp[i] for i in range(0, len(hash_tmp), 4)])
        return result.upper()
