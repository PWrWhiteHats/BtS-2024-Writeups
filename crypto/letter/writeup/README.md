# Letter writeup

The encryption procedure in this challenge is basically a substitution cipher with 3 different alphabets applied on random sized blocks of text, determined by the keys_l list.
On top of that, there's a Vigenere cipher.

I've split decrypting into 3 stages: breaking Vigenere, getting keys_l, decrypting the flag.

## Stage 1: Vigenere

Let's start by stating what we know. First blocks are probably Dear Derek because that's how people usually start their messages. We also know that the first > 10 chars were encrypted with one substitution key. Then the first sentence of letter probably starts with "I". So we have two blocks of Vigenere to work with:

```python
p[0] = "DEARD"
p[1] = "EREKI"
```

Note that those blocks are "nice", because some letters appear many times. This helps us with breaking Vigenere. If we have:

```
a block b = c0c1c2c3c4 
and a key = k0k1k2k3k4
```

and the plaintext A encrypts to some cA, plaintext D to some cD etc., then we can write following equations:

```
b0 = cDcEcAcRcD
   + k0k1k2k3k4 
(those operation are done per char, i.e it is shorthand for b0_0 = cD + k0, b0_1 = cE + k1, etc)

b1 = cEcRcEcKcI 
   + k0k1k2k3k4 
```

And from that, we can create a system of equations for the Vigerene key:

```
b0_0 - b0_4 = cD + k0 - cD - k4 = k0 - k4
b0_1 - b1_0 = cE + k1 - cE - k0 = k1 - k0
b1_0 - b1_2 = cE + k0 - cE - k2 = k0 - k2
b1_1 - b0_3 = cR + k1 - cR - k3 = k1 - k3
```

The problem now is, this system is indefinite. But, we have constrained the unknowns in such a way, that they are all dependent on each other - if we guess one, we guess them all.
So should we just bruteforce it? We probably could, but it is not necessary. In fact, ANY solution to that system of equations will be enough for us. It is because the substitution keys will "amortize" that, i.e. if we choose k0' such that k0 - k0' = a where k0 is the real key, then the substitution key will become s0 + a, s1 + a etc., and we can continue with decryption all the same.

```
example:
k = BCDEF
s = 0F5W1NRTPEAX2VGLU3OSM4KDB97IQZHJY6C8
p = DEARD 

#c1 = s[p0]s[p1]s[p2]s[p3]s[p4] = W1B3W
#c2 = c1 + k = Y4F8C

we take our equations, fix k0 = A, and solve for the rest:
k' = ABCDE
so we use it to decrypt:
p1 = c2 - k' = X2C4X = c1 + 1
so the substitution key becomes s + 1:
s = 1G6X2OSUQFBY3WHMV4PTN5LECA8UR0IKX7D9
```

So, we just fix k0 = a, and decrypt the Vigenere cipher.

## Stage 2: block lengths

This is where we get to the more tedious (but much easier) part. We just need to figure out what are the block lengths. To do that, we can start with substituting the known plaintext values for the first sub_key ("dear derek") and looking where else in the text there are some comprehensible words.

E.g I found out that the second last block is also encrypted with the first key, and the block seems to end on "regar". So the next block from "ds" must be encrypted with a different key, because the "D" value didn't decrypt. 

After substituting some more we can clearly see the blocks encrypted with different keys. In the end, we can conclude that key lengths were `[10,12,10,12]`.

## Stage 3: Win

Now all thats left to do is substituting as many characters as we can to complete our substitution keys. Then, we can recover the flag. The flag contains numbers (as it is written in leetspeak) and there were not that many numbers in the letter, but those can be easily guessed given the context and letters around them.