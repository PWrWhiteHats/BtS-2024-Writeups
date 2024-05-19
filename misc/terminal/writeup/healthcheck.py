import pwnlib.tubes

r = pwnlib.tubes.remote.remote('127.0.0.1', 1337)
d = r.recvuntil(b'Last login: ', timeout=5)

if not d or d != b'Last login: ':
    r.close()
    exit(1)

r.close()

exit(0)
