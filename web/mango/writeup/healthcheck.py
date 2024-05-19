#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import requests


def basic():
      r = requests.get('http://localhost:3000/api-docs/')
      return r.status_code == 200 and "swagger-ui" in r.text


def nosql():
      r = requests.get('http://localhost:3000/fruits?id[$ne]=661c4cf05717c55d8ceb5d23')

      if r.status_code != 200 or "frutti" not in r.text:
            print("NoSQL failed")
            return False

      return True


if basic() and nosql():
      exit(0)

exit(1)
