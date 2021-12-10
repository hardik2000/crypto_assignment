# pip install pycryptodome
from Crypto.Util.number import getPrime


def key_write():
    X = getPrime(4)
    Y = getPrime(4)

    with open("BT18CSE118_SE_Z_Sk.txt", "w") as f:
        f.write(f"{X} {Y}")


if __name__ == "__main__":
    key_write()
