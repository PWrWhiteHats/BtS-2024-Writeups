you can't read the flag located in ```/root```, no cap
##### Connection info:
After starting an instance, use [sc](https://github.com/CTFd/snicat) to bind it to the port on your machine:
```
sc -b <local_port> <instance_subdomain.instance_domain>
```
After that, you can connect to an instance with ssh:
```
ssh btsbob@localhost -p <local_port>
```
Password: password
