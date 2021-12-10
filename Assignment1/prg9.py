"""
Name : Hardik
Enrollment No. : BT18CSE118

Instruction to run:
    python prg9.py a m
    
    eg: python prg9.py 4 7
    o/p: 3 
"""

# importing sys module to use sys.argv for taking command line arguments
import sys

# algorithm to calculate gcd of two numbers
def gcd(a, b):
    if b == 0:
        return a
    return gcd(b, a % b)


# function to compute all factors of number m
def factors_fun(m):
    i = 1
    ret = []
    while i * i <= m:
        if m % i == 0:
            ret.append(i)
            if m // i != i:
                ret.append(m // i)
        i += 1
    return ret


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


# ord(a mod m) -> min t such that a^t= congruent to 1 mod m
def ord(a, m, n):
    # variable to store gcd(a,m)
    g = gcd(a, m)
    if g != 1:
        return -1
    res = 1

    # phi m approach
    divisors = factors_fun(n)
    # print(divisors)
    divisors.sort()
    prev = a
    if prev % m == 1:
        return 1
    for k in range(1, len(divisors)):
        now = pow(a, divisors[k] - divisors[k - 1], m)

        if (prev * now) % m == 1:
            return divisors[k]
        prev = (prev * now) % m

    # iterative approach
    # k = 1
    # while k < m:
    #     res = (res * a) % m
    #     if res == 1:
    #         return k
    #     k += 1

    return -1


if __name__ == "__main__":
    a = int(sys.argv[1])
    m = int(sys.argv[2])
    phi = eular_totient_fun(m)

    t = ord(a, m, phi)

    print(t, end="")

