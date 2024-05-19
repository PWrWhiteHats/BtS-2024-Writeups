from PIL import Image

enc1 = Image.open('../challenge/img1.png')
enc2 = Image.open('../challenge/img2.png')
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
