This challenge is about reverse engineering a virtual machine implementation written in Rust
which will enable player to analyze the given program bytecode and manipulate it to get the flag.

### Challenge Input
- `little_rusty` binary which is a statically linked ELF file of the VM implementation \
  which reads a program from a file end executes it,
- `program.bts` file which is the program with the flag hidden inside.

### Goal
The goal is to manipulate the program or the VM so it doesn't get stuck and prints the flag.

### VM architecture
```
- push <value> - 0xCB
- pop          - 0xF5
- print        - 0xD2
- xor <key>    - 0x64
- add <value>  - 0x79
- mul <value>  - 0x7A
- jmpf <value> - 0xDB (jump forward)
- jmpb <value> - 0xBD (jump backward)
- nop          - 0x4F
```

### Problem Overview
`program.bts` bytecode execution consists of three stages: \
printing the beginning of the flag, getting stuck, printing the rest of the flag. \
Program gets stuck because there is a nop slide into a jmpb (jump backward) instruction after printing the first part of the flag.

### Solution
Intended solution is to patch the jump instruction and the appropriate value to a nop instruction.

Script which does that (modifies the program file):
```python
with open("program.bts", "rb") as f:
    bytecode = list(f.read())

# patch out jump and the value to NOP
bytecode[135] = 0x4f
bytecode[136] = 0x4f

with open("program.bts", "wb") as f:
    f.write(bytes(bytecode))
```

### Flag
BtSCTF{Ru5t_r3v3rs1ng_b3_l1ke}


### *Not-intended* solution
Notice that program hides flag with the following sequence of instructions:  
push(char1)  
xor(key1,top(stack))  
push(char2)  
xor(key2,top(stack)  
...  

Thus we find all xor instructions and xor whatever comes after and before xor instruction like so:
```py
from functools import reduce
from itertools import islice
from operator import add
from pathlib import Path
from pwn import xor
import collections

# expecting program.bts in cwd
program = Path("program.bts").read_bytes()

def do_xor(window):
    return xor(window[0], window[2])

def is_xor(window):
    return window[1] == 0x64

def sliding_window(iterable, n):
    it = iter(iterable)
    window = collections.deque(islice(it, n - 1), maxlen=n)
    for x in it:
        window.append(x)
        yield tuple(window)

print(
    reduce(add, filter(bytes.isascii, map(do_xor, filter(is_xor, sliding_window(program, 3))))).decode()
)
```

