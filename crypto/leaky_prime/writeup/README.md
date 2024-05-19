# Writeup

The easiest way is to get the data, calculate (or read from source) how many bits are missing. Because it's a small number, we can brute-force them and check if the result yields two prime numbers - our `p` and `q`. Then calculate `d` and decrypt.

```
from pwn import *
from Crypto.Util.number import inverse, long_to_bytes, isPrime

URL = '127.0.0.1'
PORT = 1337
PRIMESIZE = 512
e = 65537

io = remote(URL,PORT)

ct = int(io.recvline().decode().strip())
n = int(io.recvline().decode().strip())
msb = io.recvline().decode().strip()
missing_bits = PRIMESIZE - len(msb)
log.info(f'{missing_bits=}')

for i in range(pow(2,missing_bits)):
    lsb = bin(i)[2:].zfill(missing_bits)
    p = int(msb + lsb,2)
    
    if not isPrime(p):
        continue
    q = n // p
    
    if not isPrime(q):
        continue

    if p*q != n:
        continue
    log.info(f'{p=}')
    log.info(f'{q=}')
    break

tot = (p-1)*(q-1)
d = inverse(e, tot)
m = pow(ct,d,n)
log.success(long_to_bytes(m).decode())
```