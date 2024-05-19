## walls - writeup

If you read the whole description, you can possibly rule out most common steganography techniques. Of course you can also confirm it with online analysers such as [StegOnline](https://georgeom.net/StegOnline). The link in the description redirects to wikipedia article on the BMP file format, to information about pixel storage in the BMP. There is a lot information, but one bit is crucial - if the length of a scanline in bytes is not a multiple of 4, padding has to be added. What's more - padding does not have to be zeroed out. That means we can hide data in padding that will not be visible to the user. To get the flag, you have to write a script that will extract the padding:

```python
scanline_size = 497 * 3 # we multiply by 3 because 1 pixel = 24 bits
padding_size = 4 - ((497 * 3) % 4) 
cursor = 54 # pixel array offset

with open("challenge.bmp", "rb") as f:
    data = f.read()

extracted = b""
while cursor < len(data) - scanline_size:
    cursor += scanline_size
    extracted += data[cursor].to_bytes(1, "big")
    cursor += padding_size

flag = ''.join([chr(x) for x in extracted if 32 <= x <= 128])
print(flag)
```
Output:
```
BtSCTF{actually_im_in_your_padding_hehe_4311728187}
```