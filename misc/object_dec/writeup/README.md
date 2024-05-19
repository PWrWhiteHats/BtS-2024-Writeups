### Writeup object_dec

In this challenge, we have intercepted a poorly encrypted JSON containing credentials of a hacker group named `caesar`. The objective is to decrypt the given encrypted string using a Caesar cipher and extract the flag. The encrypted string is provided, and the flag format is `BtSCTF{...}`.

### Caesar Cipher Decryption
The provided Python solution utilizes a simple Caesar cipher decryption function (`rot13`). The `rot13` function shifts each character by 13 positions in the alphabet. It is applied to both lowercase and uppercase letters, leaving other characters unchanged.

### Challenge Input
The encrypted string:
```python
encrypted = "rlW1p2IlozSgMFV6VaOupTS5LGVkZmpvYPNvpTSmp3qipzDvBvNvDaEGD1ETr3xjqI9lZmZmoUysL3WeMS90nQAsLmDmpmElsFW9sd"
```

### Challenge Output
The expected output is the decrypted string in base64 encoding, which is then decoded to reveal the flag in the format `BtSCTF{...}`.

### Solution Code
```python
import base64

def rot13(s):
    # Implementation of Caesar cipher (ROT13)

encrypted = "rlW1p2IlozSgMFV6VaOupTS5LGVkZmpvYPNvpTSmp3qipzDvBvNvDaEGD1ETr3xjqI9lZmZmoUysL3WeMS90nQAsLmDmpmElsFW9sd"

# Decrypt the Caesar cipher and decode from base64 (might require adding '==' for paddding)
decrypted_bytes = base64.b64decode(rot13(encrypted+"=="))

# Print the decrypted flag
print(decrypted_bytes)
```

### Flag Decryption
Running the provided code will print the decrypted bytes, which, when decoded from base64, will reveal the flag in the specified format.

### Note
The Caesar cipher is a basic encryption technique, and the ROT13 variant is a special case where the shift is 13 positions. This type of cipher is relatively easy to break, and more secure encryption methods should be used for sensitive information in real-world scenarios.