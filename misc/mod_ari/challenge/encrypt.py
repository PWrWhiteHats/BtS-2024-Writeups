# BtSCTF{zhong_guo_sh3n_gyu_din_gli}
flag = "BtSCTF{zhong_guo_sh3n_gyu_din_gli}"
flag_bytes = flag.encode()
flag_int = int.from_bytes(flag_bytes)

primes = [2137, 1000039, 1000081, 1000099, 1000000033,	1000000087, 1000000093, 1000000007, 10000000019, 100000000003, 100000000019, 100000000057]
residues = []
k = 1
for prime in primes:
    residues.append(flag_int % prime)
    k *= prime

print("Values")
print(f"bigint decipher = {int.to_bytes(flag_int, (flag_int.bit_length() + 7) // 8, 'big')}")
print(f"flag_int={flag_int}")
if flag_int > k:
    raise ValueError("Moduli product must be greater than flag_int for the solution to be unique")
print("Ticket info")
print("### mod-ari\n"
      "For reasons unbeknown to humankind our target decided to encode a flag by using pairs of integers.\n"
      "We managed to obtain some of them.\n"
      "Can you find the flag?\n\n"
      f"a_i = {residues}\n\n"
      f"m_i = {primes}\n"
      "\n> `BtSCTF{?????_???_????_???_???_???}`"
      )