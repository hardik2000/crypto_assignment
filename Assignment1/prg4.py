"""
Name : Hardik
Enrollment No. : BT18CSE118

Instruction to run:
    python prg4.py m
    eg : python prg4.py 11
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


# RRSMm algoroithm
def RRSM(m):
    rrsm_set = []
    cnt = 0
    fact = factors_fun(m)

    if len(fact) == 2:
        if fact[0] == 1 and fact[1] == m:
            rrsm_set = [x for x in range(1, m)]
            cnt = m - 1

    else:
        for i in range(1, m):
            for j in fact:
                if i % j == 0:
                    if gcd(i, m) == 1:
                        rrsm_set.append(i)
                        cnt += 1
                    break
    return cnt, rrsm_set


if __name__ == "__main__":
    m = int(sys.argv[1])
    n, rrsm_set = RRSM(m)
    rrsm_set.sort()
    for i in rrsm_set:
        print(i, end=" ")
    print(n, end="")
