This challenge introduces the Okamoto signature scheme with biased nonces. The point of the challenge was to use hidden number problem in order to exploit those biases.

We want to calculate `x1 - x2`. First look at the signature creation procedure:

```python
a = entropy & ((1 << ((l // 2) - 1)) - 1)
b = entropy >> ((l // 2) - 1)

r1 = (r + a) % q
r2 = (r + b) % q
```
...

```python
s1 = (r1 + x1*h) % q
s2 = (r2 + x2*h) % q
```
if we subtract s1 - s2 we get:

```python
s1 - s2 = a - b + (x1 - x2) * h
(x1 - x2) = ((s1 - s2) + (b - a)) / h 
```
so, to calculate `(x1 - x2)` we first need to calculate `(b - a)`, as its much easier due to the fact that `b > a` and `bitlen(a) ~= bitlen(b) = bitlen(q)/2` i.e. a nd b are small and suitable to be found using lattice solutions to hidden number problem. 

To create our instance of HNP, we will use the two signatures that we received in output txt
```python
s1 = (r1 + x1*h) % q
s2 = (r2 + x2*h) % q

(x1 - x2) = ((s1 - s2) + (b1 - a1)) / h1 
```
```python
s3 = (r3 + x1*h) % q
s4 = (r4 + x2*h) % q

(x1 - x2) = ((s3 - s4) + (b2 - a2)) / h2
```

so:

```python
((s3 - s4) + (b2 - a2)) / h2 = ((s1 - s2) + (b1 - a1)) / h1
```

and after some transformations:

```python
(b2 - a1) + (s3 - s4) - (s1 - s2) * h2 / h1 - (b1 - a1) * h2/ h1 = 0 mod q
```

recall that you can instantiate HNP to solve e.g. the following problem (it is used for breaking DSA/ECDSA with biased nonces):

```python
y1 + t*y2 + u = 0 mod q
```
where t,y are known and y1,y2 are small. In our case:

```python
y1 = (b2 - a2)
y2 = (b1 - a1)
t = - h2 / h1 
u = (s3 - s4) - (s1 - s2) * h2 / h1
```

Then we just plug it into a matrix and solve for k1,k2:

```python
t = (- h2 * inverse_mod(h1, q)) % q
u = ((s3 - s4) - (s1 - s2) * h2 * inverse_mod(h1, q)) % q

K = 2 ** 128 # upper bound on b-a

B = matrix(ZZ, [
    [q, 0, 0],
    [t, 1, 0],
    [u, 0, K]
])

shortest_vector = [row for row in B.BKZ() if K in row][0] # we know that the shortest vector contains K
```

then we just plug the calculated y2 into the equation
```python
(x1 - x2) = ((s1 - s2) + (b1 - a1)) / h1 
```
and we're done:

```python
y1 = abs(shortest_vector[0])
y2 = abs(shortest_vector[1])

delta = ((s1 - s2 + y2) * inverse_mod(h1, q)) % q # x1 - x2

key = hash([delta]).to_bytes(32, "big")
cipher = AES.new(key, AES.MODE_CBC, iv=flag_enc[:16])
pt = unpad(cipher.decrypt(flag_enc[16:]), 16)
```