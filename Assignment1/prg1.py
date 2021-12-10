"""
Name : Hardik
Enrollment No. : BT18CSE118

Instruction to run:
    python prg1.py n a1 a2 a3 ..... an.
"""

# importing sys module to use sys.argv for taking command line arguments
import sys

# algorithm to calculate gcd of two numbers
def gcd(a, b):
    if b == 0:
        return a
    return gcd(b, a % b)


# algorithm to calculate common divisor of n numbers
def common_divisor(n, arr):
    # variable to store gcd
    var_gcd = arr[0]
    comm_div = dict()

    # finding gcd of n numbers
    for i in range(1, n):
        var_gcd = gcd(arr[i], var_gcd)

    # finding divisors of that gcd
    for i in range(1, var_gcd + 1):
        if i * i > var_gcd:
            break
        if (var_gcd % i) == 0:
            comm_div[i] = 1
            if (var_gcd // i) != i:
                comm_div[var_gcd // i] = 1
    # printing all space seperated common divisors
    comm_div = [i for i in sorted(comm_div)]
    for i in range(len(comm_div) - 1):
        print(comm_div[i], end=" ")
    print(comm_div[-1], end="")


if __name__ == "__main__":
    n = int(sys.argv[1])
    arr = sys.argv[2:]
    arr = list(map(int, arr))
    common_divisor(n, arr)
