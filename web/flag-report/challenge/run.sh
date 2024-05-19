#!/bin/sh

echo 0.0.0.0 googlechromelabs.github.io >> /etc/hosts
echo 0.0.0.0 plausible.io >> /etc/hosts

flask run -h 0.0.0.0 &
flask --app bot run -h 0.0.0.0 -p 5001
