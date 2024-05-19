In this challenge, our objective is to decode a flag that has been encoded using pairs of integers. The given information includes two lists: `a_i` representing the residues and `m_i` representing the corresponding moduli. The flag is encoded in the form `BtSCTF{?????_???_?????}`.

The provided Python solution employs the Chinese Remainder Theorem (CRT) to decipher the flag from the given residues and moduli. Let's break down the steps of the solution:

### Chinese Remainder Theorem (CRT)
The Chinese Remainder Theorem is a mathematical technique that allows us to find a solution to a system of simultaneous modular congruences. In this case, it is applied to the pairs of integers (`a_i`, `m_i`).

The CRT algorithm involves the following steps:
1. Calculate the product of all moduli (`prod`).
    2. For each pair (`n_i`, `a_i`), calculate `p` as `prod` divided by `n_i`.
    3. Accumulate the sum of `a_i * mul_inv(p, n_i) * p` for each pair.
    4. Return the final result modulo `prod`.

### Modular Inverse
The `mul_inv` function calculates the modular inverse of an integer `a` with respect to a modulus `b`. It is a crucial part of the CRT algorithm. This function ensures that the modular inverse is computed correctly for each modulus in the system.

### Flag Decoding
After applying the CRT, the resulting integer is converted back to bytes using `int.to_bytes`. The size of the output is determined by the bit length of the integer. Finally, the decoded flag is printed.

### Challenge Input
The challenge provides two lists:
```python
a_i = [1609, 961662, 917667, 557244, 931717056, 927153951, 178868775, 372965939, 3738025605, 6922527163, 53305961088, 94034742228]
m_i = [2137, 1000039, 1000081, 1000099, 1000000033, 1000000087, 1000000093, 1000000007, 10000000019, 100000000003, 100000000019, 100000000057]
```

### Challenge Output
The provided Python solution outputs the decoded flag in integer and byte formats.

### Solution Code
```python
from functools import reduce
from operator import mul

def chinese_remainder_theorem(m, a):
    sum = 0
    prod = reduce(mul, m)
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
```

By running the provided code, the flag will be decoded and printed in the required format: `BtSCTF{?????_???_?????}`.