"""
    HARDIK
    BT18CSE118
    $           python3 BT18CSE118_AC_B_Kg.py

"""
import os

# from Crypto.Util.number import getPrime
from Prime_Generator import getPrime
import random
import json

# algorithm to calculate gcd of two numbers
def gcd(a, b):
    if b == 0:
        return a
    return gcd(b, a % b)


# function to return pair (a,b) where a is prime number and b is power of a in factorization
def prime_factorizations(m):
    fact = []
    cnt = 0
    # check with 2
    while m % 2 == 0:
        m = m // 2
        cnt += 1
    if cnt > 0:
        fact.append([2, cnt])

    # check for other number from 3 onwards that are odd and less then sqrt(a)
    i = 3
    cnt = 0
    while (i * i) <= m:
        cnt = 0
        while m % i == 0:
            m = m // i
            cnt += 1
        if cnt > 0:
            fact.append([i, cnt])
        i += 2

    # if m is prime
    if m > 2:
        fact.append([m, cnt + 1])
    return fact


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


# eular totient function to calculate phi(m)
def eular_totient_fun(m):
    prime_fact = prime_factorizations(m)
    phi = 1
    for i, j in prime_fact:
        phi *= pow_mod(i, j) - pow_mod(i, j - 1)
    return int(phi)


# function to compute all factors of number m
def factors_fun(m):
    i = 1
    ret = []
    while i * i <= m:
        if m % i == 0:
            ret.append(i)
            if m / i != i:
                ret.append(m // i)
        i += 1
    ret.sort()
    return ret


# RRSMm algoroithm
def RRSM(m):
    phi = eular_totient_fun(m)
    rrsm_set = []
    fact = factors_fun(m)
    if len(fact) == 2:
        if fact[0] == 1 and fact[1] == m:
            rrsm_set = [x for x in range(1, m)]
    else:
        for i in range(1, m):
            for j in fact:
                if i % j == 0:
                    if gcd(i, m) == 1:
                        rrsm_set.append(i)
                    break
    return phi, rrsm_set


def key_generation():
    p = getPrime(16)  # no of bit = 16
    print("prime number p is ", p)
    phi, rrsm_set = RRSM(p)
    e1 = random.choice(rrsm_set)
    d = random.randint(1, phi)
    print("phi ", phi, " len(rrsm_set) ", len(rrsm_set))
    e2 = pow_mod(e1, d, p)
    ret = {}
    ret["pk"] = [e1, e2, p]
    ret["sk"] = [d, p]
    print("e1 ", e1, " e2 ", e2, " d ", d)
    return ret


def key_write(keys):
    with open("BT18CSE118_AC_B_Sk.txt", "w") as f:
        f.write(json.dumps(keys))


def key_read():
    with open("BT18CSE118_AC_B_Sk.txt", "r") as f:
        keys = json.load(f)
    return keys


if __name__ == "__main__":
    keys = key_generation()
    key_write(keys)
    keys = key_read()

