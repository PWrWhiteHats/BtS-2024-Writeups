FROM fedora:latest

RUN /usr/sbin/useradd -u 1000 user

RUN dnf install ca-certificates socat libseccomp-devel -y

WORKDIR /home/user/
COPY flag bin /home/user/

RUN chown root:root flag bin 
RUN chmod 444 flag bin
RUN chown user:user /home/user
RUN chmod 755 /home/user

RUN chmod a+x /home/user/bin

EXPOSE 1331

USER user

CMD   socat \
      TCP-LISTEN:1331,reuseaddr,fork \
      EXEC:"timeout 120 /home/user/bin"