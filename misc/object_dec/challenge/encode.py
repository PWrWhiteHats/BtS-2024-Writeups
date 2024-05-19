import base64
import codecs

flag = "BtSCTF{y0u_r333ly_crkd_th3_c43s4r}"
object = '{"username":"papaya2137", "password": "' + flag + '"}'
cipher = base64.b64encode(object.encode())


print(codecs.encode(str(cipher), "rot13"))