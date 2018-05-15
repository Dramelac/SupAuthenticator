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
        if self.__aes is None:
            raise Exception("Authenticator is not initialize")

        nowtime = time.time()
        nowtime -= nowtime % 30
        chall = str(nowtime) + self.__hash

        hash = hashlib.sha256(chall.encode("utf-8")).hexdigest()

        ciphered = self.__aes.encrypt(hash)
        base = base64.b64encode(ciphered)

        hash = hashlib.md5(base).hexdigest()

        result = ''.join([hash[i] for i in range(0, len(hash), 4)])
        return result.upper()
