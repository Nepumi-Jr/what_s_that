from random import randint

def shuffle(arr):
    n = len(arr)
    for i in range(n):
        j = randint(0, n - 1)
        arr[i], arr[j] = arr[j], arr[i]

def sample_int(n, m, n_sample):
    l = []
    while len(l) < n_sample:
        x = randint(n, m)
        if x not in l:
            l.append(x)

    return l