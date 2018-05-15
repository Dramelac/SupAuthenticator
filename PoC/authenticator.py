import base64

from Crypto.Cipher import AES
import time
import hashlib


class Authenticator:

    def __init__(self, key):
        self.__aes = AES.new(key, AES.MODE_CBC)
        self.__cache_hash(key)

    def __cache_hash(self, key):
        m = hashlib.sha256()
        m.update(key.encode("utf-8"))
        self.__hash = m.digest()

    def generate_token(self):
        if self.__aes is None:
            raise Exception("Authenticator is not initialize")

        nowtime = time.time()
        nowtime -= nowtime % 30
        chall = str(nowtime) + self.__hash

        m = hashlib.sha256()
        m.update(chall.encode("utf-8"))
        hash = m.digest()

        ciphered = self.__aes.encrypt(hash)
        base = base64.b64encode(ciphered)

        m = hashlib.md5()
        m.update(base)
        hash = m.digest()

        result = ''.join([hash[i] for i in range(0, len(hash), 2)])
        result.upper()
        return result
