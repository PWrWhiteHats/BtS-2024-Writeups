FROM alpine:latest

RUN apk add --no-cache \
    gdb \   
    bash \
    nano \
    python3 \
    libcap \
    procps \
    openssh-server \
    net-tools \
    netcat-openbsd \
    curl

RUN setcap cap_sys_ptrace=eip /usr/bin/gdb
RUN adduser -D -s /bin/bash btsbob && echo "btsbob:password" | chpasswd
RUN mkdir /var/run/sshd
WORKDIR /etc/ssh
RUN ssh-keygen -A
COPY scripts .
RUN chmod +x challenge_manager.sh entrypoint.sh
RUN echo "BtSCTF{gdbussin_fr_fr_no_cap_7843477187}" > flag.txt
RUN chmod 400 flag.txt

EXPOSE 22

CMD ["./entrypoint.sh"]