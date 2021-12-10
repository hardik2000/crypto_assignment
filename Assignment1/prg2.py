"""
Name : Hardik
Enrollment No. : BT18CSE118

Instruction to run:
    python prg2.py a b
"""

# importing sys module to use sys.argv for taking command line arguments
import sys

# algorithm to calculate gcd of two numbers
def gcd(a, b):
    if b == 0:
        return a
    print(a, b)
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


if __name__ == "__main__":
    a = int(sys.argv[1])
    b = int(sys.argv[2])
    # a, b = max(a, b), min(a, b)
    # g, x, y = extended_euclidean(a, b)
    # # x = (x % b + b) % b
    # print(x, end=" ")
    # print(y, end="")
    gcd(a, b)

