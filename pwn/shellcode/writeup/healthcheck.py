#!/usr/bin/env python3

from subprocess import run, PIPE

stdout = run(["bash", "-c", "cat shellcode_raw | nc localhost 1331"], text=True, stdout=PIPE).stdout
assert "BtSCTF" in stdout