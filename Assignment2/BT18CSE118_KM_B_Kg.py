from Crypto.Random import get_random_bytes


def key_generation():
    KA = get_random_bytes(8)
    KB = get_random_bytes(8)
    return KA, KB


def key_write(KA, KB):
    with open("BT18CSE118_KM_B_ASk.txt", "wb") as f:
        f.write(KA)
    with open("BT18CSE118_KM_B_BSk.txt", "wb") as f:
        f.write(KB)


def key_read():
    with open("BT18CSE118_KM_B_ASk.txt", "rb") as f:
        KA = f.readlines()
    with open("BT18CSE118_KM_B_BSk.txt", "rb") as f:
        KB = f.readlines()
    return KA, KB


if __name__ == "__main__":
    KA, KB = key_generation()
    print(KA, KB)
    key_write(KA, KB)
    KA, KB = key_read()
    print(KA, KB)

