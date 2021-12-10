"""
	HARDIK
	BT18CSE118
"""
from random import randrange, getrandbits


def is_prime(p, k=256):
    """ Test if a number is prime
        return True if n is prime
    """
    # Test if p is not even.
    if p == 2 or p == 3:
        return True
    if p <= 1 or p % 2 == 0:
        return False
    # find r and s
    s = 0
    r = p - 1
    while r & 1 == 0:
        s += 1
        r //= 2
    # do k tests
    while k > 0:
        k -= 1
        a = randrange(2, p - 1)
        temp = pow(a, r, p)
        if temp != 1 and temp != p - 1:
            j = 1
            while j < s and temp != p - 1:
                temp = pow(temp, 2, p)
                if temp == 1:
                    return False
                j += 1
            if temp != p - 1:
                return False
    return True


def getPrime(no_of_bits=4):
    p = 4
    while not is_prime(p):
        p = getrandbits(no_of_bits)
        p |= (1 << no_of_bits - 1) | 1
    return p


# print(getPrime(1024))
