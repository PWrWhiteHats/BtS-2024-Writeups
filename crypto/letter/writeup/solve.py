
from string import ascii_uppercase, digits  

alphabet = ascii_uppercase + digits

with open("./challenge/letter.txt", "r") as f:
    letter = f.read()

enc = letter

# so the encryption first uses substition with 3 different keys
# on random sized blocks of text, determined by the keys_l list
# then it uses a Vigenere cipher with a key of length 5

def sub_mod(ct1, key_x):
    ct2 = ""
    i = 0
    for c in ct1:
        if c in alphabet:
            ix = (alphabet.index(c) - alphabet.index(key_x[i % len(key_x)])) % len(alphabet)
            ct2 += alphabet[ix]
            i += 1
        else:
            ct2 += c
    return ct2

vig_key_len = 5

enc_stripped = enc.replace(" ", "").replace("\n", "").replace(",", "").replace("'", "").replace(".", "").replace("-", "")

blocks = [enc_stripped[i:i+vig_key_len] for i in range(0, len(enc_stripped), vig_key_len)]

# FIRST STAGE, Vigenere

# first block is probably Dear Derek because that's how people usually start their messages
# we also know that the first > 10 chars were encrypted with one substitution key

# then it has to start with "I"...

# cribs
p = [_ for _ in range(len(enc))]
p[0] = "DEARD"
p[1] = "EREKI" # Dear Derek, I...

# if a block b = c0c1c2c3c4 
# and key      = k0k1k2k3k4
# and we know that plaintext A encrypts to some cA (the first key is used for > 10 chars), 
# plaintext D to some cD etc
# then we can write following equations:
# b0 = cDcEcAcRcD
#    + k0k1k2k3k4 
# (those operation are done per char, i.e it is shorthand for b0_0 = cD + k0, b0_1 = cE + k1, etc)
# 
# b1 = cEcRcEcKcI 
#    + k0k1k2k3k4 

# so, we can write a following system of equations:
# b0_0 - b0_4 = cD + k0 - cD - k4 = k0 - k4
# b0_1 - b1_0 = cE + k1 - cE - k0 = k1 - k0
# b1_0 - b1_2 = cE + k0 - cE - k2 = k0 - k2
# b1_1 - b0_3 = cR + k1 - cR - k3 = k1 - k3
# now all the k's are constrained. If we guess 1 we guess them all
# we cannot really bruteforce as the "plaintext" is kinda random.

# but we dont really even have to. Due to the constraints, no matter which xor key
# we choose it will be ok. It is because the substitution keys will "amortize" that, i.e.
# if we choose k0' such that k0 - k0' = a where k0 is the real key, then the substitution key will become
# s0 + a, s1 + a etc., which doesn't really matter in the end.

# More bluntly: if we choose vigenere key k' = k0 - a, then the substitution key will become s' = s + a
# for the same plaintext-ciphertext pairs.

# example:
# k = BCDEF
# s = 0F5W1NRTPEAX2VGLU3OSM4KDB97IQZHJY6C8
# p = DEARD 

#c1 = s[p0]s[p1]s[p2]s[p3]s[p4] = W1B3W
#c2 = c1 + k = Y4F8C

# we take our equations, fix k0 = A, and solve for the rest:
# k' = ABCDE
# so we use it to decrypt:
# p1 = c2 - k' = X2C4X = c1 + 1
# so the substitution key becomes s + 1:
# s = 1G6X2OSUQFBY3WHMV4PTN5LECA8UR0IKX7D9
# and we can still decrypt the message

k0 = alphabet[0]
k0 = alphabet.index(k0)
k1 = alphabet.index(blocks[0][1]) - alphabet.index(blocks[1][0]) + k0
k2 = alphabet.index(blocks[1][2]) - alphabet.index(blocks[1][0]) + k0
k3 = alphabet.index(blocks[0][3]) - alphabet.index(blocks[1][1]) + k1
k4 = alphabet.index(blocks[0][4]) - alphabet.index(blocks[0][0]) + k0
vig_key = [k0, k1, k2, k3, k4]
vig_key = [alphabet[k % len(alphabet)] for k in vig_key] 

# try constructing a decryption key 1. We don't 
# know much about it, so we need to dig deeper
c_test = sub_mod(enc, vig_key)
sub_key = ["" for _ in alphabet]
sub_key[alphabet.index("D")] = c_test[0]
sub_key[alphabet.index("E")] = c_test[1]
sub_key[alphabet.index("A")] = c_test[2]
sub_key[alphabet.index("R")] = c_test[3]
sub_key[alphabet.index("K")] = c_test[9]
sub_key[alphabet.index("I")] = c_test[13]

p_test = [alphabet[sub_key.index(c)].lower() if c in alphabet and c in sub_key else (c.upper() if c not in sub_key and c in alphabet else c) for c in c_test]
p_test = "".join(p_test)

print(vig_key)
print(p_test)

p_test = [alphabet[sub_key.index(c)].lower() if c in alphabet and c in sub_key else ("." if c not in sub_key and c in alphabet else c) for c in c_test]
p_test = "".join(p_test)
print(p_test)

# SECOND STAGE, start substitution

# now we can clearly see some words.
# we can also start using freq analysis, but it wont really be of much help as we dont know the key lengths yet.
# we can probably use index of coincidence to guess the key lengths, but we can also just guess them.

# in my case:
# found BEST REGARDS, seems that the key ends on regar|
sub_key[alphabet.index("G")] = "B"
sub_key[alphabet.index("B")] = "L"
sub_key[alphabet.index("S")] = "1"
sub_key[alphabet.index("T")] = "N"

# found celebrating
sub_key[alphabet.index("C")] = "F"
sub_key[alphabet.index("L")] = "8"
#sub_key[alphabet.index("N")] = "0"
#sub_key[alphabet.index("G")] = "J"

# found there
sub_key[alphabet.index("H")] = "S"

# found well
sub_key[alphabet.index("W")] = "O"

# looking forward...
sub_key[alphabet.index("O")] = "0"

# found everyone
sub_key[alphabet.index("V")] = "9"
sub_key[alphabet.index("Y")] = "Q"
sub_key[alphabet.index("N")] = "J"
# flag
sub_key[alphabet.index("F")] = "3"

sub_key2 = ["" for _ in alphabet]
sub_key2[alphabet.index("O")] = "Z"

# second key has Alice
sub_key2[alphabet.index("A")] = "S"
sub_key2[alphabet.index("L")] = "9"
sub_key2[alphabet.index("I")] = "U"
sub_key2[alphabet.index("C")] = c_test[0]
sub_key2[alphabet.index("E")] = "Q"

# hope 
sub_key2[alphabet.index("H")] = "Y"
sub_key2[alphabet.index("O")] = "I"
sub_key2[alphabet.index("P")] = "K"
sub_key2[alphabet.index("E")] = "Q"

# this
sub_key2[alphabet.index("T")] = "6"
sub_key2[alphabet.index("H")] = "Y"
sub_key2[alphabet.index("I")] = "U"
sub_key2[alphabet.index("S")] = "W"

# regards
sub_key2[alphabet.index("D")] = "A"
#while
sub_key2[alphabet.index("W")] = "M"

# since
sub_key2[alphabet.index("S")] = "H"

# looking is under that last key
sub_key3 = ["" for _ in alphabet]
sub_key3[alphabet.index("L")] = "5"
sub_key3[alphabet.index("O")] = "Z"
sub_key3[alphabet.index("K")] = "M"
sub_key3[alphabet.index("I")] = "R"
sub_key3[alphabet.index("N")] = "L"
sub_key3[alphabet.index("G")] = "6"

# letter
sub_key3[alphabet.index("E")] = "S"
sub_key3[alphabet.index("R")] = "9"

# finds you 
sub_key3[alphabet.index("F")] = "A"
sub_key3[alphabet.index("D")] = "2"
sub_key3[alphabet.index("S")] = "C"
sub_key3[alphabet.index("Y")] = "O"
sub_key3[alphabet.index("U")] = "F"

p_test = [alphabet[sub_key.index(c)].lower() if c in alphabet and c in sub_key else (c.upper() if c not in sub_key and c in alphabet else c) for c in c_test]
p_test = "".join(p_test)

print(p_test)

p_test = [alphabet[sub_key.index(c)].lower() if c in alphabet and c in sub_key else ("." if c not in sub_key and c in alphabet else c) for c in c_test]
p_test = "".join(p_test)
print(p_test)

# THIRD STAGE, find keys_l and the rest of substitution keys

# from the words I assume that one of keys_l is 12.
# also Im suspecting that the letter starts with I hope..., and H is known for key 1
# while hope is not decrypted. so the first key length must be 10
# first is 10, second is 12 for sure
# third is also 10
# last is 12? funny
keys_l = [10, 12, 10, 12]
keys_s = [sub_key, sub_key2, sub_key3]

sub_key[alphabet.index("P")] = "W"
sub_key[alphabet.index("Q")] = "7"
sub_key[alphabet.index("U")] = "V"
sub_key[alphabet.index("J")] = "D"
sub_key[alphabet.index("M")] = "X"
sub_key[alphabet.index("X")] = "5"
sub_key2[alphabet.index("S")] = "W"
sub_key2[alphabet.index("N")] = "H"
sub_key2[alphabet.index("M")] = "G"
sub_key2[alphabet.index("U")] = "E"
sub_key2[alphabet.index("B")] = "1"
sub_key2[alphabet.index("Y")] = "2"
sub_key2[alphabet.index("F")] = "V"
sub_key2[alphabet.index("R")] = "T"
sub_key3[alphabet.index("W")] = "3"
sub_key2[alphabet.index("N")] = "H"
sub_key3[alphabet.index("G")] = "0"
sub_key3[alphabet.index("M")] = "G"
sub_key3[alphabet.index("H")] = "K"
sub_key3[alphabet.index("A")] = "X"
sub_key3[alphabet.index("H")] = "K"
sub_key3[alphabet.index("T")] = "P"
sub_key3[alphabet.index("P")] = "B"
sub_key3[alphabet.index("V")] = "E"
sub_key3[alphabet.index("B")] = "D"

# now we can just decrypt the flag as we see the words there
# we know its probably leetspeak and we know that
# missing chars all mostly numbers, because we got most of the letters already
sub_key[alphabet.index("4")] = "M"
sub_key[alphabet.index("1")] = "6"
sub_key[alphabet.index("3")] = "R"
sub_key2[alphabet.index("0")] = "D"
sub_key2[alphabet.index("4")] = "J"
sub_key2[alphabet.index("7")] = "3"
sub_key2[alphabet.index("G")] = "0"
sub_key2[alphabet.index("1")] = "7"
sub_key2[alphabet.index("3")] = "C"
sub_key3[alphabet.index("1")] = "V"
sub_key3[alphabet.index("7")] = "W"
sub_key3[alphabet.index("4")] = "J"
sub_key3[alphabet.index("0")] = "4"
sub_key3[alphabet.index("G")] = "6"


p_test = ""
ii = 0
k1 = 0
k2 = 0
i = 0
for c in c_test.upper():
    if c in alphabet:
        if ii >= keys_l[k1]:
            ii = 0
            k1 = (k1 + 1) % len(keys_l)
            k2 = (k2 + 1) % len(keys_s)
            p_test += f"|{k2 + 1}|"
        if c not in keys_s[k2]:
            i += 1
            ii += 1
            p_test += c.upper()
            continue
        p_test += alphabet[keys_s[k2].index(c)].lower()
        i += 1
        ii += 1
    else:
        p_test += c

p_test = "".join(p_test)
print(p_test)

