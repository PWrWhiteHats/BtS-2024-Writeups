#!/usr/bin/env python3
from pwnlib.tubes.ssh import ssh

s = ssh(user="bts-bob", password="password", host="localhost", port=22)
output = s("ps -eaf | grep challenge_manager.sh").decode()
# if there is not a challenge_manager process started by root, user might have killed it - restart needed
if "root" in output:
    exit(0)
exit(1)
