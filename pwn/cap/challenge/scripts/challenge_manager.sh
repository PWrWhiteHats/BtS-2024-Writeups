#!/bin/bash

while true; do
    python3 ./very_important_script.py
    wait $!
    sleep 1
done