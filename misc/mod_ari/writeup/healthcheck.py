from functools import reduce


def chinese_remainder_theorem(m, a):
    sum = 0
    prod = reduce(lambda acc, b: acc * b, m)
    for n_i, a_i in zip(m, a):
        p = prod // n_i
        sum += a_i * mul_inv(p, n_i) * p
    return sum % prod


def mul_inv(a, b):
    return pow(a,-1,b)


residues = [1609, 961662, 917667, 557244, 931717056, 927153951, 178868775, 372965939, 3738025605, 6922527163, 53305961088, 94034742228]
primes = [2137, 1000039, 1000081, 1000099, 1000000033, 1000000087, 1000000093, 1000000007, 10000000019, 100000000003, 100000000019, 100000000057]
flag_int = chinese_remainder_theorem(primes, residues)
print(flag_int)
print(int.to_bytes(flag_int, (flag_int.bit_length() + 7) // 8, 'big'))