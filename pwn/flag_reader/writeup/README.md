# Write-up

If you want to see the binary ask it to print the flag_reader file.  

To print flag encode "flag.txt" as $'\x66\x6c\x61\x67\x2e\x74\x78\x74'.
This will allow you to use `.` character.

```sh
echo JCdceDY2XHg2Y1x4NjFceDY3XHgyZVx4NzRceDc4XHg3NCc= | base64 -d | ./flag_reader
``