"""
Name : Hardik
Enrollment No. : BT18CSE118

Instruction to run:
    python prg3.py a
"""

# importing sys module to use sys.argv for taking command line arguments
import sys
import math

# algorithm to print prime factors in increasing order
def prime_factors(a):
    ans = []
    # check with 2
    while a % 2 == 0:
        ans.append(2)
        a = a // 2
        flg = 1
    # check for other number from 3 onwards that are odd and less then sqrt(a)
    i = 3
    while (i * i) <= a:
        flg = 0
        while a % i == 0:
            ans.append(i)
            flg = 1
            a = a // i
        i += 2
    # if a is prime
    if a > 2:
        ans.append(a)
    for i in range(len(ans) - 1):
        print(ans[i], end=" ")
    print(ans[-1], end="")


if __name__ == "__main__":
    a = int(sys.argv[1])
    prime_factors(a)
