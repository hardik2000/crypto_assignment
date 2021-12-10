"""
Name : Hardik
Enrollment No. : BT18CSE118

Instruction to run:
    python prg8.py a b m
    
eg:
python prg8.py 606 138 1710
Y 178 463 748 1033 1318 1603

python prg8.py 2 5 7 4 2 6 1 3 5    
Y 83 188
    
"""

# importing sys module to use sys.argv for taking command line arguments
import sys

# algorithm to calculate gcd of two numbers
def gcd(a, b):
    if b == 0:
        return a
    return gcd(b, a % b)


# function to check whether all m[i] are pair wise co prime or not
def pairwise_co_prime(m):
    N = 1
    lcm = 1
    for i in range(len(m)):
        N *= m[i]
        lcm = (lcm * m[i]) // gcd(lcm, m[i])

    return N, bool(N == lcm)


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


# function to calculate multiplicative inverse
def inv_fun(a, b):
    g, x, y = extended_euclidean(a, b)
    res = (x % b + b) % b
    return res


def CRT_fun_util(a, b, m, n, i, a_i, m_i, N, ans_arr):
    if i == n:
        ans = 0
        for j in range(n):
            temp_1 = a_i[j] % m_i[j]
            temp_2 = inv_fun(N // m_i[j], m_i[j])

            ans = (ans + ((N // m_i[j]) * temp_1 * temp_2) % N) % N
        ans_arr.append(ans % N)
        # print(a, b, m, n, i, a_i, m_i, N, ans_arr)
        return True
    else:

        g = gcd(a[i], m[i])
        # print(a, b, m, n, i, a_i, m_i, N, ans_arr, g)
        if b[i] % g != 0:
            return False
        else:
            if g == 1:
                a_i_inv = inv_fun(a[i], m[i])
                temp = (b[i] * a_i_inv) % m[i]
                a_i.append(temp)
                m_i.append(m[i])
                if CRT_fun_util(a, b, m, n, i + 1, a_i, m_i, N, ans_arr) == False:
                    return False
                a_i.pop()
                m_i.pop()
            else:
                g, x, y = extended_euclidean(a[i], m[i])
                x = (x % m[i] + m[i]) % m[i]
                b[i] = ((b[i] * x) // g) % m[i]
                for k in range(g):
                    a_i.append((b[i] + (k * (m[i] // g))) % m[i])
                    m_i.append(m[i])
                    if CRT_fun_util(a, b, m, n, i + 1, a_i, m_i, N, ans_arr) == False:
                        return False
                    a_i.pop()
                    m_i.pop()
            return True


def CRT_fun(a, b, m):
    exist = " "
    N, flg = pairwise_co_prime(m)
    if flg:
        n = len(m)
        ans = []
        flg = CRT_fun_util(a, b, m, n, 0, [], [], N, ans)
        if flg == False:
            exist = "N"
            print(exist, end=" ")
        else:
            exist = "Y"
            print(exist, end=" ")
            ans.sort()
            for x in range(len(ans) - 1):
                print(ans[x] % N, end=" ")
            print(ans[-1], end="")

    else:
        exist = "N"
        print(exist, end="")


if __name__ == "__main__":
    a = []
    b = []
    m = []
    k = 1
    n = int(sys.argv[1])
    while k <= 3 * n:
        a.append(int(sys.argv[k + 1]))
        b.append(int(sys.argv[k + 2]))
        m.append(int(sys.argv[k + 3]))
        k += 3

    CRT_fun(a, b, m)

