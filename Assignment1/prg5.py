"""
Name : Hardik
Enrollment No. : BT18CSE118

Instruction to run:
    python prg5.py a x n
    eg python prg5.py 5 596 1234
    ans=1013
    
"""

# importing sys module to use sys.argv for taking command line arguments
import sys

# function to compute the binary representation of the number
def bin_rep(a):
    k = []
    while a > 0:
        k.append(a % 2)
        a = a // 2
    return k


# function to check if n is prime or not
def is_prime(n):
    i = 2
    if n % i == 0:
        return False
    i += 1
    while i * i <= n:
        if n % i == 0:
            return False
        i += 2

    if n <= 1:
        return False

    return True


# function to compute the value
def solve(a, x, n):
    b = 1
    if x == 0:
        return b
    A = a

    # using fermet's theorem to reduce x i.e. a^(p-1) mod p = 1
    if is_prime(n):
        temp = x % (n - 1)
        x = min(x, temp)
    k = bin_rep(x)

    if k[0] == 1:
        b = a
    # print(0, k[0], A, b)
    for i in range(1, len(k)):
        A = (A * A) % n
        if k[i] == 1:
            b = (A * b) % n
        # print(i, k[i], A, b)

    return b


if __name__ == "__main__":
    a = int(sys.argv[1])
    x = int(sys.argv[2])
    n = int(sys.argv[3])
    ans = solve(a, x, n)
    print(ans, end="")
