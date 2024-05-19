FROM fedora:latest

RUN /usr/sbin/useradd -u 1000 user

RUN dnf install ca-certificates socat -y

WORKDIR /home/user/
COPY flag.txt flag_reader /home/user/
COPY fake_flag flag

RUN chown root:root flag.txt flag flag_reader 
RUN chmod 444 flag.txt flag
RUN chown user:user /home/user
RUN chmod 755 /home/user

RUN chmod a+x /home/user/flag_reader

EXPOSE 1338

USER user

CMD   socat \
      TCP-LISTEN:1338,reuseaddr,fork \
      EXEC:"timeout 120 /home/user/flag_reader"
