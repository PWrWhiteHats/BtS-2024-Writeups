# Copyright 2020 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
FROM alpine:latest

RUN apk update 

COPY flag /
COPY ca.crt /
COPY ca.key /

COPY requirements.txt /requirements.txt
RUN apk add --no-cache python3 py3-pip ca-certificates openssl tshark socat libcap

RUN setcap cap_net_raw+eip /usr/bin/dumpcap

RUN pip install -r /requirements.txt --break-system-packages
RUN pip install gunicorn --break-system-packages

COPY ca.crt /usr/local/share/ca-certificates/ca.crt
RUN chmod 644 /usr/local/share/ca-certificates/ca.crt
RUN update-ca-certificates

# Generate certificates
RUN openssl req -new -nodes -out cert_forum.csr -newkey rsa:2048 -keyout cert_forum.key -subj '/CN=Silly Forum/C=AT/ST=Wroclaw/L=Wroclaw/O=Silly Co' -addext "subjectAltName=IP:127.0.0.1" 
RUN openssl req -new -nodes -out cert_image.csr -newkey rsa:2048 -keyout cert_image.key -subj '/CN=Silly Image/C=AT/ST=Wroclaw/L=Wroclaw/O=Silly Co' -addext "subjectAltName=IP:127.0.0.1" 

RUN openssl x509 -req -in cert_forum.csr -CA ca.crt -CAkey ca.key -CAcreateserial -out cert_forum.crt -days 730 -copy_extensions copyall -sha256
RUN openssl x509 -req -in cert_image.csr -CA ca.crt -CAkey ca.key -CAcreateserial -out cert_image.crt -days 730 -copy_extensions copyall -sha256

COPY mitm /mitm
COPY forum-app /forum-app
COPY image-app /image-app

COPY run.sh /
RUN chmod +x run.sh

EXPOSE 5000 8888

ENV REQUESTS_CA_BUNDLE=ca.crt

CMD /run.sh