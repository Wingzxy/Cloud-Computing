from init import multi_upload
import sys


def gpfs(time, confidence):
    if time < 60:
        print("Can't find a golden nonce")
    else:
        multi_upload(8, 8)


if __name__ == '__main__':
    t = sys.argv[1]
    T = int(t)
    l = sys.argv[2]
    L = int(l)
    gpfs(T, L)
