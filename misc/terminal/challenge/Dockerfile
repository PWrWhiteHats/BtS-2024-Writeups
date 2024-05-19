FROM python:3.11.9-slim-bookworm as chroot

RUN apt update -y
RUN apt install -y socat redis-server
RUN /usr/sbin/useradd --no-create-home -u 1000 user

WORKDIR /home/user/
COPY requirements.txt /home/user/
RUN pip3 install -r requirements.txt

COPY server.py /home/user/
COPY config.json /home/user/
COPY prompt.txt /home/user/
COPY start.sh /home/user/
COPY handle_connection.sh /home/user/

RUN chown -R user:user /home/user
USER user

CMD ["./start.sh"]
