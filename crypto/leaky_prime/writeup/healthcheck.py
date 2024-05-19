#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import re
import socket
import uuid


def basic():
      HOST = "127.0.0.1"
      PORT = 1337

      with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((HOST, PORT))
            data = s.recv(1024)
            if not data:
                  return False
            return True


if basic():
      exit(0)

exit(1)
