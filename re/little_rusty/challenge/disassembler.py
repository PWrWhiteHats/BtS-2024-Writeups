#!/usr/bin/env python

import sys

if len(sys.argv) < 2:
    print(f"Usage: {sys.argv[0]} <file>")
    exit(1)

program_file = sys.argv[1]

with open(program_file, "rb") as f:
    prog_bytes = f.read()
    i = 0
    while i < len(prog_bytes):
        cur_instruction = prog_bytes[i]
        match cur_instruction:
            case 0xCB:
                i += 1
                print(f"{hex(prog_bytes[i - 1])} {hex(prog_bytes[i])}\t=>  push {hex(prog_bytes[i])}")
            case 0xF5:
                print(f"{hex(prog_bytes[i])}\t\t=>  pop")
            case 0xD2:
                print(f"{hex(prog_bytes[i])}\t\t=>  print")
            case 0x64:
                i += 1
                print(f"{hex(prog_bytes[i - 1])} {hex(prog_bytes[i])}\t=>  xor {hex(prog_bytes[i])}")
            case 0x79:
                i += 1
                print(f"{hex(prog_bytes[i - 1])} {hex(prog_bytes[i])}\t=>  add {hex(prog_bytes[i])}")
            case 0x7A:
                i += 1
                print(f"{hex(prog_bytes[i - 1])} {hex(prog_bytes[i])}\t=>  mul {hex(prog_bytes[i])}")
            case 0xDB:
                i += 1
                print(f"{hex(prog_bytes[i - 1])} {hex(prog_bytes[i])}\t=>  jmpf {hex(prog_bytes[i])}")
            case 0xBD:
                i += 1
                print(f"{hex(prog_bytes[i - 1])} {hex(prog_bytes[i])}\t=>  jmpb {hex(prog_bytes[i])}")
            case 0x4F:
                print(f"{hex(prog_bytes[i])}\t\t=>  nop")
            case _:
                pass
        i += 1
