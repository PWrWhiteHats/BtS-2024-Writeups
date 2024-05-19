# Solve

1. Verify whether there is any data inside using steghide: `steghide info totally_awesome_animal.jpg`, use blank password.
2. Something's inside, get it out: `steghide --extract -sf totally_awesome_animal.jpg`
3. Analyze contents of extracted file:
    - `file hidden`
    - `xxd hidden`
    - `hexdump hidden`
4. As observed in the hexdumps, there is 32 `\x01` bytes inserted in front of legitimate 7z archive, this can be further confirmed by running data carving tools, suchs as `binwalk hidden`
5. Extract archive without the preceding bytes. Two proposed techniques:
    - `dd if=hidden bs=1 of=tmp.out skip=32`
    - `binwalk --dd=".*" hidden`

For next steps, lets assume first way, so resulting file is `tmp.out`.

6. Inspect file again, `file hidden` returns a 7z archive.
7. Inspect using dedicated tool: `7z l tmp.out` shows a `flag.txt` being hidden inside.
8. Try extracting: `7z x tmp.out`. As 7zip prompts for password, it's evident that archive is encrypted (also seen in previous command's output).
9. Generate a hash suitable for cracking: `7z2john tmp.out`. Save it in a file, here we use `hash.txt`. You should save only the hash, so part of the output starting with `$` onwards
10. Run a hashcat against the hash: `hashcat hash.txt /path/to/rockyou`. Notes:
    - default rockyou path on kali machine is under `/usr/share/wordlists/rockyou.txt`, it is probably gzipped if you never used it before or are on fresh install.
    - should hashcat autodetection not work, use `hashcat hash.txt /path/to/rockyou -m 11600`
11. Decrypt the archive again, this time using password: `7z x tmp.out`
12. `cat flag.txt` 
