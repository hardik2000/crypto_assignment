"""
Name : Hardik
Enrollment No. : BT18CSE118

Instruction to run:
    python prg7.py a b m
    
    eg: python prg7.py 606 138 1710
    o/p: Y 6 178 463 748 1033 1318 1603 
"""

# importing sys module to use sys.argv for taking command line arguments
import sys

# algorithm to calculate gcd of two numbers
def gcd(a, b):
    if b == 0:
        return a
    return gcd(b, a % b)


# extended euclidean algoroithm
def extended_euclidean(a, b):
    if b == 0:
        return a, 1, 0
    x2 = 1
    x1 = 0
    y2 = 0
    y1 = 1

    # algorithm as per book 2.107
    while b > 0:
        q = a // b
        r = a - q * b
        x = x2 - q * x1
        y = y2 - q * y1
        a = b
        b = r
        x2 = x1
        x1 = x
        y2 = y1
        y1 = y
    return a, x2, y2


def cal_beta(a, b, m, g):
    return b // g


def cal_alpha_inv(a, b, m, g):
    alpha = a // g
    mue = m // g
    g, x, y = extended_euclidean(alpha, mue)
    res = (x % mue + mue) % mue
    return res


def cal_mue(a, b, m, g):
    return m // g


def sol_congruence(a, b, m):
    g = gcd(a, m)
    exist = " "
    sol = []
    if b % g == 0:
        exist = "Y"
        mue = cal_mue(a, b, m, g)
        print(mue)
        beta = cal_beta(a, b, m, g)
        print(beta)
        alpha = cal_alpha_inv(a, b, m, g)
        print(alpha)
        x = (beta * alpha + mue) % mue
        print(x)
        for i in range(g):
            sol.append(x + (i * mue))
    else:
        exist = "N"
    return exist, len(sol), sol


if __name__ == "__main__":
    a = int(sys.argv[1])
    b = int(sys.argv[2])
    m = int(sys.argv[3])

    exist, g, sol = sol_congruence(a, b, m)
    print(g)
    sol.sort()
    if exist == "Y":
        print(exist, end=" ")
        print(g, end=" ")
        for i in range(len(sol) - 1):
            print(sol[i], end=" ")
        print(sol[-1], end="")
    else:
        print(exist, end="")
