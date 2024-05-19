#!/bin/bash

if [[ -z $1 ]]; then
        echo "No file to process! Usage: ./chall_create <filename.jpg>"
        exit
fi

echo "BtSCTF{g3t_0ut_0f_my_h34d_lm4000}" > flag.txt

7z a -t7z -m0=lzma -mx=9 -mfb=64 -md=32m -ms=on -psamantha archive.7z flag.txt

python3 -c "print(32*'\x01', end='')" > hidden
cat archive.7z >> hidden

steghide --embed -ef hidden -cf $1 -sf $1_hidden -p ""

rm -rf archive.7z hidden flag.txt
