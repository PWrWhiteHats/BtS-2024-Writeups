#!/usr/bin/env python

# push <value> - 0xCB
# pop          - 0xF5
# print        - 0xD2
# xor <key>    - 0x64
# add <value>  - 0x79
# mul <value>  - 0x7A
# jmpf <value> - 0xDB
# jmpb <value> - 0xBD
# nop          - 0x4F

FLAG = open("./flag").read().strip()
XOR_KEY = 162


with open("./program.bts", "wb") as f:

    def push(val):
        f.write(b"\xCB" + val.to_bytes(1))

    def pop():
        f.write(b"\xF5")

    def print():
        f.write(b"\xD2")

    def xor(val):
        f.write(b"\x64" + val.to_bytes(1))

    def add(val):
        f.write(b"\x79" + val.to_bytes(1))

    def mul(val):
        f.write(b"\x7A" + val.to_bytes(1))

    def jmpf(val):
        f.write(b"\xDB" + val.to_bytes(1))

    def jmpb(val):
        f.write(b"\xBD" + val.to_bytes(1))

    def nop():
        f.write(b"\x4F")

    for c in FLAG[:7]:
        push(ord(c) ^ XOR_KEY)
        xor(XOR_KEY)
        print()
        XOR_KEY = (XOR_KEY + 37) % 255

    for i in range(100):
        nop()
    jmpb(37)

    for c in FLAG[7:]:
        push(ord(c) ^ XOR_KEY)
        xor(XOR_KEY)
        print()
        XOR_KEY = (XOR_KEY + 37) % 255

    push(ord("\n"))
    print()
