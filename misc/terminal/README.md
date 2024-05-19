We discovered a new open port. It looks like a Linux terminal, but something feels off.
Could you connect to it and see what's going on?
##### Connection info:
After starting an instance, use [sc](https://github.com/CTFd/snicat) to bind it to the port on your machine:
```
sc -b <local_port> -insecure terminal.wh.edu.pl
```
