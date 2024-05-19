### Writeup for xor_img

Flag: **BtSCTF{t0ld_y0u_th3y_u53d_1t_tw1c3}**

In this challenge, the target has encrypted two images using a one-time pad (OTP) encryption scheme, which involves XOR-ing each pixel of the images with a shared key. The goal is to retrieve the flag, which is expected to be in the format `BtSCTF{?????????}`. The provided solution utilizes Python and the Python Imaging Library (PIL) to decrypt the images.

### One-Time Pad (OTP) Encryption
The OTP encryption scheme involves XOR-ing each byte of the plaintext with a corresponding byte of a secret random key. In this scenario, both images (`img1.png` and `img2.png`) are encrypted using the same key. When XOR-ing two ciphertexts encrypted with the same key, the result is the XOR of the original plaintexts. Hence, XOR-ing the encrypted images results in the XOR of the original images.

```
(img1 xor key) xor (img2 xor key) = img1 xor im2g, because key xor key = 0.
```

### Challenge Input
Two encrypted images: `img1.png` and `img2.png`
 
### Challenge Output
The expected output is the decrypted image saved as `solve.png`, and the flag in the format `FLAG{?????????}`.

### Solution Code
```python
from PIL import Image

enc1 = Image.open('./img1.png')
enc2 = Image.open('./img2.png')
width, height = enc1.size

enc1_pixel = enc1.load()
enc2_pixel = enc2.load()

res_dec = Image.new("RGB", (width, height))
red_dec_pixel = res_dec.load()

for y in range(height):
    for x in range(width):
        enc1_r, enc1_g, enc1_b = [int(k) for k in enc1_pixel[x, y]]
        enc2_r, enc2_g, enc2_b = [int(k) for k in enc2_pixel[x, y]]
        red_dec_pixel[x, y] = enc1_r ^ enc2_r, enc1_g ^ enc2_g, enc1_b ^ enc2_b

res_dec.save('./solve.png')
```

### Flag Retrieval
The decrypted image (`solve.png`) can be viewed, and the flag should be extracted from the image.
