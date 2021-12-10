import os
from Crypto.Util.number import getPrime
import random
import json


# algorithm to calculate power(x,y,p)
def pow_mod(x, y, p=float("inf")):
    res = 1

    x = x % p
    if x == 0:
        return 0

    while y > 0:
        if (y & 1) == 1:
            res = (res * x) % p
        y = y >> 1
        x = (x * x) % p

    return res


def key_generation():
    p = getPrime(32)  # no of bit = 16
    q = getPrime(32)
    print(p, q)
    n = p * q
    S = random.randint(0, n - 1)
    V = pow_mod(S, 2, n)
    return S, V, n


def key_write(S, V, n):
    with open("BT18CSE118_EA_B_Sk.txt", "w") as f:
        f.write(f"{S} {V} {n}")


def key_read():
    with open("BT18CSE118_EA_B_Sk.txt", "r") as f:
        lines = f.readlines()
    return lines[0].split(" ")


if __name__ == "__main__":
    S, V, n = key_generation()
    key_write(S, V, n)
    S, V, n = key_read()
    print(S, V, n)
