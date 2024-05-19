#!/bin/bash
redis-server --daemonize yes
socat TCP-LISTEN:1337,reuseaddr,fork EXEC:/home/user/handle_connection.sh
