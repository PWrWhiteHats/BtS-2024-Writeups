FROM debian:stable-slim

RUN apt update
RUN apt install -y openssh-server binutils cowsay vim nano gcc
RUN sed -i 's/#PermitRootLogin prohibit-password/PermitRootLogin no/' /etc/ssh/sshd_config
RUN sed -i 's/#PasswordAuthentication yes/PasswordAuthentication yes/' /etc/ssh/sshd_config
RUN sed -i 's/#Port 22/Port 43422/' /etc/ssh/sshd_config

RUN service ssh start
EXPOSE 43422

RUN useradd -m guest
RUN echo "guest:princess" | chpasswd
RUN usermod -s /bin/bash guest
RUN ssh-keygen -A

RUN echo "/home/guest/supercowsay" >> /home/guest/.bashrc

COPY supercowsay.c /home/guest
RUN gcc /home/guest/supercowsay.c -o /home/guest/supercowsay
RUN rm /home/guest/supercowsay.c
RUN chown root:root /home/guest/supercowsay
RUN chmod +s /home/guest/supercowsay

COPY flag /root/flag

CMD ["/usr/sbin/sshd", "-D"]

