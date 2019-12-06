import hashlib
import time
import sys
import multiprocessing as mp


orig_message = 'COMSM0010cloud'


# final cnd version
def a_cnd(zeros, current, p_num):
    # zeros, current, p_num = params
    target = (2 ** (256 - zeros)) - 1
    for nonce in range(current, 2**32, p_num):
        input_str = str(orig_message) + str(nonce)
        hashval = hashlib.sha256(hashlib.sha256(input_str.encode('utf-8')).digest()).hexdigest()
        if int(hashval, 16) <= target:
            print(nonce)
            # print(f'Found it! nonce is {nonce}, sha256({orig_message} + {nonce})')
            return nonce


# cnd for local multiprocessing
def c_cnd(params):
    zeros, current, p_num = params
    target = (2 ** (256 - zeros)) - 1
    for nonce in range(current, 2**32, p_num):
        input_str = str(orig_message) + str(nonce)
        hashval = hashlib.sha256(hashlib.sha256(input_str.encode('utf-8')).digest()).hexdigest()
        if int(hashval, 16) <= target:
            # print(nonce)
            # print(f'Found it! nonce is {nonce}, sha256({orig_message} + {nonce})')
            return nonce


# multiprocessing cnd
def mu_c_cnd(zeros, p_num):
    zero_list = [zeros] * p_num
    currents = range(0, p_num)
    p_nums = [p_num] * p_num
    tp = list(zip(zero_list, currents, p_nums))
    # print(tp)
    p = mp.Pool(processes=p_num)
    golden_nonce = None
    # result = p.starmap(upload1, tp)
    start = time.perf_counter()
    for result1 in p.imap_unordered(c_cnd, tp):
        if result1 != None:
            golden_nonce = result1
            break
    end = time.perf_counter()
    print(f'Computing finished in {round(end - start, 6)} second(s)')
    print(golden_nonce)
    p.close()
    p.join()


# First cnd method
def my_cnd(zeros, upper, lower):
    target = (2 ** (256 - zeros)) - 1
    for nonce in range(lower, upper):
        input_str = str(orig_message) + str(nonce)
        hashval = hashlib.sha256(hashlib.sha256(input_str.encode('utf-8')).digest()).hexdigest()
        if int(hashval, 16) <= target:
            print(nonce)
            # print(f'Found it! nonce is {nonce}, sha256({orig_message} + {nonce})')
            return nonce


# First cnd method for multiprocessing
def cnd(data):
    zeros, upper, lower = data
    target = (2 ** (256 - zeros)) - 1
    for nonce in range(lower, upper):
        input_str = str(orig_message) + str(nonce)
        hashval = hashlib.sha256(hashlib.sha256(input_str.encode('utf-8')).digest()).hexdigest()
        if int(hashval, 16) <= target:

            return nonce


# First multiprocessing
def multi_cnd(zeros, p_num):
    zero_list = [zeros] * p_num
    r = int(2 ** 32 / p_num)
    lower_list = list(range(0, p_num * r, r))
    upper_list = range(r, (p_num + 1) * r, r)
    upper_list = list(upper_list)
    upper_list[-1] = 2 ** 32
    p = mp.Pool(processes=p_num)
    tp = list(zip(zero_list, upper_list, lower_list))
    golden_nonce = None
    # result = p.starmap(upload1, tp)
    start = time.perf_counter()
    for result1 in p.imap_unordered(cnd, tp):
        if result1 != None:
            golden_nonce = result1
            break
    end = time.perf_counter()
    print(f'Computing finished in {round(end - start, 6)} second(s)')
    print(golden_nonce)
    # p.terminate()
    p.close()
    p.join()


if __name__ == '__main__':
    # start = time.perf_counter()
    start = time.perf_counter()
    a = sys.argv[1]
    b = sys.argv[2]
    c = sys.argv[3]
    a = int(a)
    b = int(b)
    # # multi_cnd(a, b)
    c = int(c)
    nonce = a_cnd(a, b, c)
    # mu_c_cnd(a, b)
    finish = time.perf_counter()
    print(f'Finished in {round(finish - start, 6)} second(s)')
# print(nonce)




