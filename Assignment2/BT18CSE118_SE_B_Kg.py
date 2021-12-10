from Crypto.Random import get_random_bytes
import os


def key_write(key, IV):
    with open("BT18CSE118_SE_B_Sk.txt", "wb") as f:
        f.write(key)
        f.write(b"\n")
        f.write(IV)


def key_read():
    with open("BT18CSE118_SE_B_Sk.txt", "rb") as f:
        lines = f.readlines()
    key = lines[0]
    IV = lines[1]
    return key, IV


if __name__ == "__main__":
    key = get_random_bytes(8)
    IV = os.urandom(32)
    print(key, IV)
    key_write(key, IV)
    key_r, IV_r = key_read()
    print(key_r, IV_r)
