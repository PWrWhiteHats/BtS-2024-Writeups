# Write-up
The program logs results of flag character comparisons e.g.

```sh
$ echo "BtSCTF{Never_Gonna_Give_You_Up}" | ./bin run
What is the flag?
(66 1)
(116 1)
(83 1)
(67 1)
(84 1)
(70 1)
(123 1)
(97 0)
```

Thus it's possible to brute force it with simple [script](solve.py).