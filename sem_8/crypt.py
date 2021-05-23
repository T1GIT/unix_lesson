from decimal import Decimal
import os
import random as rnd
import json

ENCODING = "utf-8"


class BytesTranslatable:
    def get_bytes(self) -> bytes:
        pass

    @staticmethod
    def parse_bytes(bts: bytes):
        pass


class Key(BytesTranslatable):
    AMOUNT_NUM = 5
    INT_RANGE = [10 ** (AMOUNT_NUM - 1), (10 ** AMOUNT_NUM) - 1]
    PATH = os.path.abspath(os.path.join("..", "keys"))

    def dump(self):
        pass

    @staticmethod
    def restore():
        pass

    @staticmethod
    def check_exist() -> bool:
        pass

    @staticmethod
    def generate(*args):
        pass


class PrivateKey(Key):
    PATH = os.path.join(Key.PATH, "private.pem")

    def __init__(self, a: int = None):
        self.a: int = a

    def dump(self) -> None:
        with open(PrivateKey.PATH, "wb") as file:
            file.write(self.get_bytes())

    def get_bytes(self) -> bytes:
        return str(self.a).encode(ENCODING)

    @staticmethod
    def restore():
        with open(PrivateKey.PATH, "rb") as file:
            return PrivateKey.parse_bytes(file.read())

    @staticmethod
    def parse_bytes(bts: bytes):
        return PrivateKey(int(bts.decode(ENCODING)))

    @staticmethod
    def check_exist() -> bool:
        return os.path.isfile(PrivateKey.PATH)

    @staticmethod
    def generate():
        return PrivateKey(rnd.randint(*Key.INT_RANGE))


def repeat_key_gen(key: [int]):
    while True:
        for el in key:
            yield el


class PublicKey(Key):
    PATH = os.path.join(Key.PATH, "public.pem")
    _SEP = "\n"

    def __init__(self, g: int = None, p: int = None, private: PrivateKey = None):
        self.p: int = p
        self.g: int = g
        self.A: int = (g ** private.a % p) if private is not None else None

    def dump(self) -> None:
        with open(self.PATH, "wb") as file:
            file.write(self.get_bytes())

    def get_bytes(self) -> bytes:
        return PublicKey._SEP.join(map(str, (self.p, self.g, self.A))).encode(ENCODING)

    @staticmethod
    def restore():
        with open(PublicKey.PATH, "rb") as file:
            return PublicKey.parse_bytes(file.read())

    @staticmethod
    def parse_bytes(bts: bytes):
        key = PublicKey()
        key.p, key.g, key.A = tuple(map(int, bts.decode(ENCODING).split(PublicKey._SEP)))
        return key

    @staticmethod
    def check_exist() -> bool:
        return os.path.isfile(PublicKey.PATH)

    @staticmethod
    def generate(private: PrivateKey):
        return PublicKey(rnd.randint(*Key.INT_RANGE), rnd.randint(*Key.INT_RANGE), private)

    def __eq__(self, other):
        return self.p == other.p and self.g == other.g and self.A == other.A


class Message(BytesTranslatable):
    def __init__(self, data: bytes = None, crypted: bytes = None, B: int = None):
        self.data: bytes = data
        self.crypted: bytes = crypted
        self.B: int = B

    def encrypt(self, public: PublicKey):
        assert self.data is not None and self.crypted is None and self.B is None
        b: int = rnd.randint(*Key.INT_RANGE)
        self.B = public.g ** b % public.p
        K = public.A ** b % public.p
        self.crypted = bytes(map(
            lambda k, d: k ^ d,
            repeat_key_gen(Decimal(K).as_tuple().digits),
            self.data))
        self.data = None

    def decrypt(self, private: PrivateKey, public: PublicKey):
        assert self.data is None and self.crypted is not None and self.B is not None
        K = self.B ** private.a % public.p
        self.data = bytes(map(
            lambda k, d: k ^ d,
            repeat_key_gen(Decimal(K).as_tuple().digits),
            self.crypted))
        self.crypted = None
        self.B = None

    def get_bytes(self) -> bytes:
        assert self.crypted
        return json.dumps({
            "crypted": self.crypted.decode(ENCODING),
            "B": self.B
        }).encode(ENCODING)

    @staticmethod
    def parse_bytes(bts: bytes):
        obj = json.loads(bts.decode(ENCODING))
        msg = Message()
        msg.data = None
        msg.crypted = obj["crypted"].encode(ENCODING)
        msg.B = obj["B"]
        return msg
