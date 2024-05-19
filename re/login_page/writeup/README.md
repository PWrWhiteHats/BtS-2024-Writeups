# Solution

The challenge binary is a GUI application that uses [iced](https://iced.rs/) library.


The easy way:

```sh
$ strings -n 7 login_page | grep -Eo 'BtSCTF\{.*\}'
```

The hard way:  
find and unxor admin's password.  
Login with admin:7792bc33-e958-4b4e-9ec4-1ed505c0007b
