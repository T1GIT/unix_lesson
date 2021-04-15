import random as rnd


def rnd_key(length: int) -> str:
    return "".join((chr(rnd.randint(0, 65535)) for _ in range(length)))


def repeat_gen(chars: str):
    while True:
        for i in chars:
            yield i


def cesar_encrypt(text: str, offset: int) -> str:
    return "".join(map(lambda c: chr((ord(c) + offset) % 65536), text))


def cesar_hack(crypted: str) -> str:
    chars = {c: crypted.count(c) for c in set(crypted)}
    return cesar_encrypt(crypted, ord(' ') - ord(max(chars, key=chars.get)))


def vernom(text: str, key: str) -> str:
    return "".join(map(lambda k, c: chr(ord(k) ^ ord(c)), repeat_gen(key), text))


def otp(text: str) -> tuple[str, str]:
    key = rnd_key(len(text))
    return vernom(text, key), key


def blockchain(text: str, key: str, block_len: int = 5) -> tuple[str, str]:
    res = []
    v = rnd_key(block_len)
    blocks = [text[i:i+block_len] for i in range(0, len(text), block_len)]
    res.append(vernom(vernom(blocks.pop(0), v), key))
    for block in blocks:
        res.append(vernom(vernom(block, res[-1]), key))
    return "".join(res), v


def feistel_cell(text: str, func: callable, K) -> str:
    assert len(text) % 2 == 0
    L = text[:len(text) // 2]
    R = text[len(text) // 2:]
    return R + vernom(func(L, K), R)


def feistel_cell_rev(text: str, func: callable, K) -> str:
    assert len(text) % 2 == 0
    L = text[:len(text) // 2]
    R = text[len(text) // 2:]
    return func(vernom(R, L), K) + L


def feistel_web(text: str, func: callable, K, iterations: int) -> str:
    for _ in range(iterations):
        text = feistel_cell(text, func, K)
    return text


def feistel_web_rev(text: str, func: callable, K, iterations: int) -> str:
    for _ in range(iterations):
        text = feistel_cell_rev(text, func, K)
    return text
